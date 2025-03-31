# === etl/mapping_engine.py ===

def map_to_trial_model(enriched: dict) -> dict:
    """
    Maps enrichment fields to trial design and evaluation schemas.
    Will evolve into structured Pydantic TrialDesignInput + EvaluationBundle.
    """
    from etl.utils.logger import log_event

    mapped = {
        "TrialDesignInput": {
            "intervention": enriched.get("what"),
            "condition": enriched.get("what"),
            "rationale": enriched.get("why"),
            "duration": enriched.get("when"),
        },
        "EvaluationHints": enriched.get("statistical_elements", [])
    }
    log_event("MAPPING_COMPLETE", {"mapped": mapped})
    return mapped