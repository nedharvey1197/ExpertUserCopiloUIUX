"""
Copilot routes for handling trial design assistance.
"""
from fastapi import APIRouter, UploadFile, File, Body, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from io import BytesIO
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from pathlib import Path

from backend.db.connection import get_conn
from models.session_state import CopilotSessionState, FileInsight
from utils.state_updater import update_session_state
from backend.etl.pipeline_runner import PipelineRunner
from logic.fivews_initializer import get_5w_context
from backend.utils.logger import setup_logger

# Set up module logger
logger = setup_logger(__name__)

router = APIRouter()

# Initialize pipeline runner
pipeline = PipelineRunner()

# ✅ Model for session input
class SessionInput(BaseModel):
    company_name: str
    company_website: Optional[str] = None
    nct_id: Optional[str] = None

# Ensure the uploads directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload_file")
async def upload_file(
    session_id: int = Form(...),
    file: UploadFile = File(...)
):
    """
    Handle file upload and process through ETL pipeline.

    Flow:
    1. Validate session exists and get session info
    2. Save uploaded file to disk
    3. Run ETL pipeline on the file
    4. Return enrichment results

    Args:
        session_id: Active session identifier (integer)
        file: Uploaded file (PDF/DOCX/TXT)

    Returns:
        dict: Contains session_id, enrichment summary, and status message

    Raises:
        HTTPException: If session not found (404) or processing fails (500)
    """
    logger.info(f"Starting file upload processing for session {session_id}")
    logger.debug(f"File details - Name: {file.filename}, Content-Type: {file.content_type}")

    try:
        # 1. Get session info from database
        logger.info("Fetching session info")
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT company_name, company_website, nct_id FROM copilot.sessions WHERE id = %s",
            (session_id,)
        )
        session = cur.fetchone()
        if not session:
            logger.error(f"Session {session_id} not found")
            raise HTTPException(status_code=404, detail="Session not found")

        company_name, company_website, nct_id = session
        logger.debug(f"Session info - Company: {company_name}, Website: {company_website}, NCT ID: {nct_id}")

        # 2. Save file
        logger.info("Saving uploaded file")
        file_location = UPLOAD_DIR / f"{session_id}_{file.filename}"
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
            logger.debug(f"Saved file to {file_location} ({len(content)} bytes)")

        # 3. Run enrichment pipeline
        logger.info("Starting ETL pipeline")
        pipeline_results = await pipeline.run_pipeline(
            document_paths=[str(file_location)],
            website_url=company_website,
            nct_id=nct_id
        )
        logger.debug("Pipeline completed successfully")

        # 4. Prepare and return response
        response = {
            "session_id": session_id,
            "summary": pipeline_results,
            "message": "Copilot enrichment complete."
        }
        logger.info(f"File processing completed for session {session_id}")
        return response

    except Exception as e:
        logger.error(f"Failed to process file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()

@router.post("/session")
async def create_session(session: SessionInput):
    """Create a new copilot session."""
    logger.info(f"Creating new session for company: {session.company_name}")
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Initialize Copilot session state
        init_state = CopilotSessionState(session_id=None).model_dump()
        logger.debug(f"Initialized session state: {init_state}")

        cur.execute("""
            INSERT INTO copilot.sessions (
                company_name,
                company_website,
                nct_id,
                state,
                created_at
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            session.company_name,
            session.company_website,
            session.nct_id,
            json.dumps(init_state),
            datetime.utcnow()
        ))

        session_id = cur.fetchone()[0]
        conn.commit()

        return {
            "session_id": session_id,
            "company_name": session.company_name,
            "created_at": datetime.utcnow().isoformat(),
            "state": init_state
        }

    except Exception as e:
        logger.error(f"Failed to create session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()

@router.post("/session/{session_id}/files")
async def upload_files(
    session_id: int,
    files: List[UploadFile] = File(...)
):
    """Handle file uploads and process through ETL pipeline."""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")

        conn = get_conn()
        cur = conn.cursor()

        # Validate session exists
        cur.execute(
            "SELECT company_name FROM copilot.sessions WHERE id = %s",
            (session_id,)
        )

        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Session not found")

        upload_results = []
        for file in files:
            # Save file and create upload record
            file_path = f"uploads/{session_id}/{file.filename}"
            Path(f"uploads/{session_id}").mkdir(parents=True, exist_ok=True)

            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)

            cur.execute(
                """
                INSERT INTO copilot.uploads (
                    session_id,
                    file_name,
                    file_path,
                    uploaded_at
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    session_id,
                    file.filename or "unnamed_file",  # Ensure we never pass None
                    file_path,
                    datetime.utcnow()
                )
            )

            upload_id = cur.fetchone()[0]

            # Process file through pipeline
            pipeline_results = await pipeline.run_pipeline(document_paths=[file_path])

            upload_results.append({
                "upload_id": upload_id,
                "file_name": file.filename,
                "pipeline_results": pipeline_results
            })

        conn.commit()
        return upload_results

    except Exception as e:
        logger.error(f"Failed to upload files: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()

@router.get("/session/{session_id}/files")
async def get_files(session_id: int):
    """Get files associated with a session."""
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Get uploads with insights
        cur.execute(
            """
            SELECT
                u.id,
                u.file_name,
                u.file_path,
                u.uploaded_at,
                fi.insights
            FROM copilot.uploads u
            LEFT JOIN copilot.file_insights fi ON fi.upload_id = u.id
            WHERE u.session_id = %s
            ORDER BY u.uploaded_at DESC
            """,
            (session_id,)
        )

        files = []
        for row in cur.fetchall():
            files.append({
                'upload_id': row[0],
                'file_name': row[1],
                'file_path': row[2],
                'uploaded_at': row[3].isoformat(),
                'insights': row[4]
            })

        return files

    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()
