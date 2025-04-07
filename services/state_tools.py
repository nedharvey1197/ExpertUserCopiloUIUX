from utils.state_updater import update_session_state
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def safe_patch_session(session_id: str, updates: dict, stage: Optional[str] = None):
    try:
        update_session_state(session_id, updates)
        logger.info(f"[{stage}] State updated: {updates}")
    except Exception as e:
        logger.error(f"[{stage}] Failed to patch session state: {e}")
        raise
