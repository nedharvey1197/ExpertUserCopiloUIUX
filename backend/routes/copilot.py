# ✅ Copilot FastAPI Endpoints (PostgreSQL)
from fastapi import APIRouter, UploadFile, File, Body, Form
from logic.fivews_initialize import get_5w_context
from pydantic import BaseModel
from typing import Optional
import psycopg2
import json
import datetime
from db.connection import get_conn
from io import BytesIO
import pandas as pd
import json
from PyPDF2 import PdfReader
from docx import Document

router = APIRouter()


# ✅ Model for session input
class SessionInput(BaseModel):
    user_id: str
    therapeutic_area: str
    trial_phase: str
    trial_condition: str
    trial_intent: Optional[str] = None
    file_summary: Optional[str] = None
    ai_insights: Optional[dict] = None

# ✅ 1. Create new Copilot session
@app.post("/copilot/session")
def create_session(session: SessionInput):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO copilot.sessions (user_id, therapeutic_area, trial_phase, trial_condition, trial_intent, file_summary, ai_insights)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        session.user_id,
        session.therapeutic_area,
        session.trial_phase,
        session.trial_condition,
        session.trial_intent,
        session.file_summary,
        json.dumps(session.ai_insights) if session.ai_insights else None
    ))
    session_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"session_id": session_id, "status": "success"}

# ✅ 2. Upload file content + parsed summary
from io import BytesIO
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from fastapi import UploadFile, File, Form

@router.post("/copilot/upload")
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
        "preview": raw_text[:300] + "..."
    }

    # Save to DB
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO copilot.uploads (session_id, filename, raw_content, parsed)
        VALUES (%s, %s, %s, %s);
    """, (
        session_id,
        filename,
        raw_text,
        None
    ))
    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "upload saved",
        "filename": filename,
        "preview": raw_text[:300] + "..." if raw_text else "(empty)"
    }

# ✅ 3. Get full Copilot summary for a session
@app.get("/copilot/summary/{session_id}")
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

@router.post("/copilot/5ws")
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
