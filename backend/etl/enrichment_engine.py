def enrich_document(parsed: dict, overrides: dict) -> dict:
    """
    Extracts trial-relevant fields from parsed raw text.
    Future versions: integrate LlamaParse, GPT, trial-specific enrichment.
    """
    from etl.utils.logger import log_event
    raw = parsed["raw_text"]
    enriched = {
        "who": "[Stub] Sponsor Name",
        "what": "[Stub] Disease / Condition",
        "why": "[Stub] Scientific rationale",
        "when": "[Stub] Duration",
        "where": "[Stub] Geographic scope",
        "statistical_elements": ["[Stub] power", "[Stub] sample size"],
    }
    log_event("ENRICHMENT_COMPLETE", {"summary": enriched})
    return enriched