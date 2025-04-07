# === etl/storage_manager.py ===

from datetime import datetime
import logging
from backend.utils.logger import log_event
from backend.db.connection import get_conn
import json

async def store_outputs(parsed: dict, enriched: dict, mapped: dict):
    """
    Store raw + enriched + mapped data into Postgres or file (MVP).
    Future: add Neo4j sync and RAG index registration.

    Flow:
    1. Log initial storage attempt
    2. Store parsed document data
    3. Store enrichment results
    4. Store mapped trial data
    5. Log completion status

    Args:
        parsed: Dictionary containing raw text and metadata
        enriched: Dictionary containing enriched data (scientific/statistical/regulatory)
        mapped: Dictionary containing mapped trial model data

    Returns:
        bool: True if storage successful
    """
    logger = logging.getLogger(__name__)

    try:
        # 1. Log storage initiation
        logger.info("Starting data storage process")
        logger.debug(f"Storage payload sizes - Parsed: {len(str(parsed))} chars, "
                    f"Enriched: {len(str(enriched))} chars, "
                    f"Mapped: {len(str(mapped))} chars")

        conn = get_conn()
        cur = conn.cursor()

        # 2. Store parsed document data
        cur.execute("""
            INSERT INTO copilot.uploads (
                raw_text,
                metadata,
                created_at
            ) VALUES (%s, %s, %s)
            RETURNING id
        """, (
            parsed.get("raw_text", ""),
            json.dumps(parsed.get("metadata", {})),
            datetime.utcnow()
        ))
        upload_id = cur.fetchone()[0]

        # 3. Store enrichment results
        cur.execute("""
            INSERT INTO copilot.file_insights (
                upload_id,
                insights,
                created_at
            ) VALUES (%s, %s, %s)
        """, (
            upload_id,
            json.dumps(enriched),
            datetime.utcnow()
        ))

        # 4. Store mapped trial data
        cur.execute("""
            INSERT INTO copilot.trial_mappings (
                upload_id,
                mapped_data,
                created_at
            ) VALUES (%s, %s, %s)
        """, (
            upload_id,
            json.dumps(mapped),
            datetime.utcnow()
        ))

        conn.commit()

        # 5. Log completion status
        log_event("STORE_OUTPUTS_COMPLETE", {
            "status": "success",
            "upload_id": upload_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        logger.info("Data storage completed successfully")
        return True

    except Exception as e:
        logger.error(f"Storage failed: {str(e)}", exc_info=True)
        log_event("STORE_OUTPUTS_ERROR", {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
        raise

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
