# ✅ Copilot FastAPI Endpoints (PostgreSQL)
from fastapi import APIRouter, UploadFile, File, Body, Form, APIRouter, HTTPException
from logic.fivews_initializer import get_5w_context
from pydantic import BaseModel
from typing import Optional
import psycopg2
import json
import datetime
from db.connection import get_conn
from io import BytesIO
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from models.session_state import CopilotSessionState  
from utils.state_updater import update_session_state

router = APIRouter()

# ✅ Model for session input
class SessionInput(BaseModel):
    company_name: str
    company_website: str
    nct_id: Optional[str] = None

@router.post("/session")
def create_session(session: SessionInput):
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Initialize Copilot session state
        init_state = CopilotSessionState().model_dump()

        cur.execute("""
            INSERT INTO copilot.sessions (
                company_name,
                company_website,
                nct_id,
                state
            ) VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (
            session.company_name,
            session.company_website,
            session.nct_id,
            json.dumps(init_state)
        ))

        session_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"session_id": session_id, "status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload_file")
async def upload_file(
    company_name: str = Form(...),
    company_website: str = Form(...),
    nct_id: str = Form(None),
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 1. Save file
        file_location = UPLOAD_DIR / f"{session_id}_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # 2. Run enrichment pipeline
        mapped_output = run_pipeline(str(file_location))

        # 3. Return enrichment summary
        return {
            "session_id": session_id,
            "summary": mapped_output,
            "message": "Copilot enrichment complete."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/raw_extract_upload_file")
async def upload_file(
    session_id: int = Form(...),
    file: UploadFile = File(...)
):
    filename = file.filename
    contents = await file.read()
    ext = filename.lower().split('.')[-1]

    raw_text = "(unsupported file type)"
    try:
        if ext == "pdf":
            reader = PdfReader(BytesIO(contents))
            raw_text = "\n".join([p.extract_text() or "" for p in reader.pages])
        elif ext == "txt":
            raw_text = contents.decode("utf-8")
        elif ext in ["csv", "tsv"]:
            df = pd.read_csv(BytesIO(contents))
            raw_text = df.to_string(index=False)
        elif ext in ["xlsx", "xls"]:
            df = pd.read_excel(BytesIO(contents))
            raw_text = df.to_string(index=False)
        elif ext == "docx":
            doc = Document(BytesIO(contents))
            raw_text = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        raw_text = f"(Error parsing file: {str(e)})"

    # Save upload + preview
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO copilot.uploads (session_id, filename, raw_content, parsed)
        VALUES (%s, %s, %s, %s);
    """, (session_id, filename, raw_text, None))
    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "upload saved",
        "filename": filename,
        "preview": raw_text[:300] + "..." if raw_text else "(empty)"
    }

# ✅ 3. Get full Copilot summary for a session
@router.get("/summary/{session_id}")
def get_summary(session_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM copilot.sessions WHERE id = %s", (session_id,))
    session = cur.fetchone()
    cur.execute("SELECT filename, raw_content, parsed FROM copilot.uploads WHERE session_id = %s", (session_id,))
    uploads = cur.fetchall()
    cur.close()
    conn.close()
    return {
        "session": session,
        "uploads": uploads,
    }



# backend/routes/copilot.py

@router.post("/5ws")
def extract_5ws(prompt: str = Body(..., embed=True)):
    structured = get_5w_context(prompt)
    return { "five_ws": structured }
# ---
# 🧪 Example `curl` commands:

# 1. Create a session
# curl -X POST http://localhost:8000/copilot/session \
#   -H "Content-Type: application/json" \
#   -d '{
#         "user_id": "ned123",
#         "therapeutic_area": "Oncology",
#         "trial_phase": "Phase 1",
#         "trial_condition": "NSCLC",
#         "trial_intent": "First-in-human dose escalation",
#         "file_summary": "Pipeline overview uploaded.",
#         "ai_insights": {"strategy": "3+3 design"}
#     }'

# 2. Upload file (form-data)
# curl -X POST http://localhost:8000/copilot/upload \
#   -F "session_id=1" \
#   -F "filename=pipeline.pdf" \
#   -F "raw_content=Full text of uploaded file..." \
#   -F 'parsed={"design": "dose escalation", "notes": "HER2+ target"}'

# 3. Retrieve full session summary
# curl http://localhost:8000/copilot/summary/1
