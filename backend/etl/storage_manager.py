# === etl/storage_manager.py ===

def store_outputs(parsed: dict, enriched: dict, mapped: dict):
    """
    Store raw + enriched + mapped data into Postgres or file (MVP).
    Future: add Neo4j sync and RAG index registration.
    """
    from etl.utils.logger import log_event
    log_event("STORE_OUTPUTS", {
        "parsed_preview": parsed["raw_text"][:100],
        "enriched_keys": list(enriched.keys()),
        "mapped_keys": list(mapped.keys())
    })
    return True
