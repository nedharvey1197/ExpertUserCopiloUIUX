FILTERS = {
    "gender": {"MALE", "FEMALE", "ALL"},
    "phase": {
        "Phase 1", "Phase 1/Phase 2", "Phase 2",
        "Phase 2/Phase 3", "Phase 3", "Phase 4"
    },
    "masking": {"DOUBLE", "NONE", "QUADRUPLE", "SINGLE", "TRIPLE"},
    "overall_status": {
        "ACTIVE_NOT_RECRUITING", "APPROVED_FOR_MARKETING", "AVAILABLE",
        "COMPLETED", "ENROLLING_BY_INVITATION", "NOT_YET_RECRUITING",
        "NO_LONGER_AVAILABLE", "RECRUITING", "SUSPENDED",
        "TEMPORARILY_NOT_AVAILABLE", "TERMINATED", "UNKNOWN",
        "WITHDRAWN", "WITHHELD"
    },
    "primary_purpose": {
        "BASIC_SCIENCE", "DEVICE_FEASIBILITY", "DIAGNOSTIC", "ECT",
        "HEALTH_SERVICES_RESEARCH", "OTHER", "PREVENTION", "SCREENING",
        "SUPPORTIVE_CARE", "TREATMENT"
    },
    "intervention_type": {
        "BEHAVIORAL", "BIOLOGICAL", "COMBINATION_PRODUCT", "DEVICE",
        "DIAGNOSTIC_TEST", "DIETARY_SUPPLEMENT", "DRUG", "GENETIC",
        "OTHER", "PROCEDURE", "RADIATION"
    }
}

def normalize_filter(field: str, value: str) -> str:
    """Normalize and validate filter input against known AACT enum sets."""
    allowed = FILTERS.get(field)
    if not allowed:
        raise ValueError(f"Unknown filter field: {field}")
    candidate = value.strip().upper() if field != "phase" else value.strip().title()
    if candidate not in allowed:
        raise ValueError(f"Invalid value '{value}' for filter '{field}'")
    return candidate
