# backend/utils/logger.py

import json
from datetime import datetime
from backend.db.connection import get_conn


def log_event(event_type: str, trial_id: str, payload: dict, user_id: str = None, version: str = "v0.1.0"):
    """
    Store a structured event log in the database (Postgres).
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO trial_analysis_logs (event_type, trial_id, user_id, version, payload, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            event_type,
            trial_id,
            user_id,
            version,
            json.dumps(payload),
            datetime.utcnow()
        )
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f"📚 Logged event: {event_type} (trial: {trial_id})")