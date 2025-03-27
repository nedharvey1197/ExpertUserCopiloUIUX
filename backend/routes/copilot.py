# ✅ Copilot FastAPI Endpoints (PostgreSQL)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import psycopg2
import json
import datetime
from dotenv import load_dotenv
import os
l
oad_dotenv()

app = FastAPI()

# 🧠 Postgres config (adjust as needed)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD", ""),  # fallback if blank
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

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
@app.post("/copilot/upload")
def upload_file(
    session_id: int = Form(...),
    filename: str = Form(...),
    raw_content: str = Form(...),
    parsed: Optional[str] = Form(None)
):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO copilot.uploads (session_id, filename, raw_content, parsed)
        VALUES (%s, %s, %s, %s);
    """, (
        session_id,
        filename,
        raw_content,
        json.dumps(json.loads(parsed)) if parsed else None
    ))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "upload saved"}

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

# ✅ Optional: CORS support for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
