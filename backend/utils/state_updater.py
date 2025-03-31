# utils/state_updater.py

import json
from db.connection import get_conn

# ✅ Generic state updater function
def update_session_state(session_id: int, updates: dict):
    conn = get_conn()
    cur = conn.cursor()

    # Fetch current state
    cur.execute("SELECT state FROM copilot.sessions WHERE id = %s", (session_id,))
    result = cur.fetchone()
    if not result:
        raise ValueError(f"No session found with ID {session_id}")

    current_state = result[0] or {}

    # Merge updates into current state (shallow merge)
    for key, value in updates.items():
        if key in current_state and isinstance(current_state[key], dict):
            current_state[key].update(value)
        else:
            current_state[key] = value

    # Persist updated state
    cur.execute(
        "UPDATE copilot.sessions SET state = %s WHERE id = %s",
        (json.dumps(current_state), session_id)
    )
    conn.commit()
    cur.close()
    conn.close()
