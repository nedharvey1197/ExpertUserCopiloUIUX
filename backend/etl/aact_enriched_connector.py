"""
Enriched AACT materialized view connector.
Queries copilot.trial_summary_mat for joined clinical trial metadata.
"""

"""
EnrichedTrialConnector (copilot/data/aact_enriched_connector.py)

This connector provides access to enriched clinical trial metadata stored in the
`copilot.trial_summary_mat` materialized view, which aggregates key fields from the
AACT database into a unified structure aligned with the Copilot's 5Ws and trial design schema.

Core Features:
--------------
- Safely queries trials by NCT ID or condition keyword (via ILIKE match)
- Supports optional filtering by validated AACT-enumerated fields (e.g., gender)
- Uses centralized input normalization via `enums_filter.py` to enforce schema-aligned values
- Returns structured trial records as dictionaries for downstream enrichment, summarization, or frontend use

Filter Safety:
--------------
All filters (e.g., gender, phase) are normalized and validated using the `normalize_filter()` utility.
This ensures resilience against user typos, schema drift, and invalid input.

Expected Use:
-------------
This class is designed to be called from Copilot session flows, background enrichment steps,
or REST API endpoints to return clinical trial metadata in a structured and consistent format.

Example Usage:
--------------
    from aact_enriched_connector import EnrichedTrialConnector

    connector = EnrichedTrialConnector()
    trial = connector.get_trial_by_nct("NCT01234567")
    results = connector.search_trials_by_condition("glioblastoma", gender="female")
"""

import logging
from typing import List, Optional, Dict, Any
from backend.db.connection import get_conn
from backend.utils.enums_filter import normalize_filter  # ✅ now using central enum validator

logger = logging.getLogger(__name__)

class EnrichedTrialConnector:
    """
    Connects to the copilot.trial_summary_mat materialized view for fast, structured trial lookups.
    """

    def __init__(self):
        self.conn = get_conn()

    def get_trial_by_nct(self, nct_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single trial by NCT ID from the materialized view."""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM copilot.trial_summary_mat WHERE nct_id = %s LIMIT 1;",
                (nct_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            colnames = [desc[0] for desc in cur.description]
            return dict(zip(colnames, row))

    def search_trials_by_condition(self, keyword: str, gender: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Search trials by keyword match in condition list or brief summary, optionally filtered by gender."""
        gender_filter = normalize_filter("gender", gender) if gender else None
        with self.conn.cursor() as cur:
            if gender_filter:
                cur.execute(
                    """
                    SELECT * FROM copilot.trial_summary_mat
                    WHERE (condition_list ILIKE %s OR brief_summary ILIKE %s)
                    AND gender = %s
                    LIMIT %s;
                    """,
                    (f'%{keyword}%', f'%{keyword}%', gender_filter, limit),
                )
            else:
                cur.execute(
                    """
                    SELECT * FROM copilot.trial_summary_mat
                    WHERE (condition_list ILIKE %s OR brief_summary ILIKE %s)
                    LIMIT %s;
                    """,
                    (f'%{keyword}%', f'%{keyword}%', limit),
                )
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return [dict(zip(colnames, row)) for row in rows]
