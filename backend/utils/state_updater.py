# utils/state_updater.py

"""
State management utilities for Copilot sessions.
Handles schema-validated updates to session state.
"""
from typing import Dict, Any
import json
import logging
from datetime import datetime
from backend.db.connection import get_conn
from models.session_state import CopilotSessionState

logger = logging.getLogger(__name__)

def update_session_state(session_id: int, update_dict: Dict[str, Any]) -> None:
    """
    Update session state with schema validation and atomic updates.

    Args:
        session_id: The session to update
        update_dict: Dictionary of updates matching CopilotSessionState schema

    Raises:
        ValueError: If update_dict doesn't match schema
        RuntimeError: If session not found or database error
    """
    try:
        # 1. Get current state
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT state FROM copilot.sessions WHERE id = %s",
            (session_id,)
        )
        result = cur.fetchone()
        if not result:
            raise ValueError(f"Session {session_id} not found")

        current_state = result[0]

        # 2. Validate and merge updates
        try:
            # Convert current state to CopilotSessionState
            current_model = CopilotSessionState(**current_state)

            # Deep merge updates
            merged_dict = {**current_model.model_dump(), **update_dict}

            # Validate merged state
            new_state = CopilotSessionState(**merged_dict)

            # Add timestamp
            new_state.last_updated = datetime.utcnow().isoformat()

        except Exception as e:
            raise ValueError(f"Invalid state update: {str(e)}")

        # 3. Atomic update
        cur.execute(
            """
            UPDATE copilot.sessions
            SET state = %s
            WHERE id = %s
            """,
            (json.dumps(new_state.model_dump()), session_id)
        )
        conn.commit()

        logger.info(f"Updated session {session_id} state")
        logger.debug(f"New state: {new_state.model_dump()}")

    except Exception as e:
        logger.error(f"Failed to update session {session_id}: {str(e)}")
        raise

    finally:
        cur.close()
        conn.close()
