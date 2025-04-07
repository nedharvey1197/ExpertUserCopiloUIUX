# backend/utils/logger.py

import json
from datetime import datetime
from backend.db.connection import get_conn
import logging
import sys
from pathlib import Path


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


def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger with both file and console handlers.

    Args:
        name: The name of the logger (usually __name__ from the calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:  # Prevent adding handlers multiple times
        logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # File handler - detailed logging
        file_handler = logging.FileHandler(log_dir / "copilot.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler - less verbose
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
