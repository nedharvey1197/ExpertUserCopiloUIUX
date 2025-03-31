# models/session_state.py

from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime

class FiveWsState(BaseModel):
    current_stage: Optional[str] = "who"
    completed: List[str] = []
    answers: Dict[str, str] = {}
    refined: Dict[str, str] = {}
    timestamp: Optional[str] = datetime.utcnow().isoformat()

class StatisticalState(BaseModel):
    population_sampled: bool = False
    method: Optional[str] = None
    test_result: Optional[Dict[str, float]] = None
    baseline_established: bool = False

class EnrichmentState(BaseModel):
    company_scraped: bool = False
    nct_parsed: bool = False
    file_uploaded: Optional[str] = None
    enriched_fields: Dict[str, str] = {}
    insights_generated: bool = False

class InteractionState(BaseModel):
    chat_history: List[Dict[str, str]] = []
    unresolved_questions: List[str] = []

class CopilotSessionState(BaseModel):
    session_id: Optional[int]
    fivews: FiveWsState = FiveWsState()
    statistics: StatisticalState = StatisticalState()
    enrichment: EnrichmentState = EnrichmentState()
    interaction: InteractionState = InteractionState()
    last_updated: str = datetime.utcnow().isoformat()