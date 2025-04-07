from fastapi import APIRouter, Query
from typing import Optional
from etl.aact_enriched_connector import EnrichedTrialConnector

router = APIRouter(prefix="/trials", tags=["Enriched Trials"])
connector = EnrichedTrialConnector()

@router.get("/by-nct")
def get_trial(nct_id: str):
    return connector.get_trial_by_nct(nct_id)

@router.get("/search")
def search_trials(
    keyword: str = Query(..., description="Condition or term to search for"),
    gender: Optional[str] = Query(None, description="Optional gender filter"),
    limit: int = Query(25, ge=1, le=100)
):
    return connector.search_trials_by_condition(keyword=keyword, gender=gender, limit=limit)
