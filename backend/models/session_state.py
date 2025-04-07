# models/session_state.py

"""
Session state models for the Copilot application.
Defines the structure for session state with focus on integrated summaries and insights.
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel
from datetime import datetime

class FileInsight(BaseModel):
    """Model for file processing insights."""
    upload_id: int
    file_name: str
    preview: Optional[str] = None
    key_findings: Dict[str, Any] = {}
    insights: Dict[str, Any]

class EnrichmentState(BaseModel):
    """Tracks document processing state and integrated insights"""
    status: str = "pending"
    file_count: int = 0
    latest_file: Optional[str] = None
    integrated_summary: Optional[str] = None
    latest_insights: Optional[FileInsight] = None
    errors: List[str] = []

class FiveWsAnswer(BaseModel):
    """Structured answer with confidence and sources"""
    answer: str
    confidence: float = 0.0
    supporting_files: List[str] = []
    last_updated: str = datetime.utcnow().isoformat()

class FiveWsState(BaseModel):
    """Integrated 5Ws analysis across all documents"""
    current_stage: str = "who"
    completed: List[str] = []
    answers: Dict[str, FiveWsAnswer] = {}
    integrated_findings: Optional[str] = None
    last_updated: str = datetime.utcnow().isoformat()

class StatisticalState(BaseModel):
    """Statistical analysis state"""
    population_sampled: bool = False
    method: Optional[str] = None
    test_result: Optional[Dict[str, float]] = None
    baseline_established: bool = False

class InteractionState(BaseModel):
    """User interaction tracking"""
    chat_history: List[Dict[str, str]] = []
    unresolved_questions: List[str] = []
    last_interaction: str = datetime.utcnow().isoformat()

class CopilotSessionState(BaseModel):
    """
    Main session state container.
    Focuses on integrated insights and summaries while detailed data stays in DB.
    """
    session_id: Optional[int] = None
    company_name: Optional[str] = None
    current_step: str = "intake"
    progress: Dict[str, Any] = {}
    fivews: FiveWsState = FiveWsState()
    statistics: StatisticalState = StatisticalState()
    enrichment: EnrichmentState = EnrichmentState()
    interaction: InteractionState = InteractionState()
    last_updated: str = datetime.utcnow().isoformat()

    class Config:
        """Pydantic model configuration"""
        json_schema_extra = {
            "example": {
                "session_id": 1,
                "enrichment": {
                    "status": "complete",
                    "file_count": 2,
                    "latest_file": "protocol_v2.pdf",
                    "integrated_summary": "Combined analysis from 2 documents shows...",
                    "latest_insights": {
                        "file_name": "protocol_v2.pdf",
                        "preview": "First 500 chars of content...",
                        "key_findings": ["Finding 1", "Finding 2"]
                    }
                },
                "fivews": {
                    "current_stage": "what",
                    "completed": ["who"],
                    "answers": {
                        "who": {
                            "answer": "Phase 1 healthy volunteers",
                            "confidence": 0.85,
                            "supporting_files": ["protocol_v1.pdf", "protocol_v2.pdf"]
                        }
                    },
                    "integrated_findings": "Cross-document analysis indicates..."
                }
            }
        }

class SessionResponse(BaseModel):
    id: str
    created_at: Optional[str]
    user_id: Optional[str]
    therapeutic_area: Optional[str]
    trial_phase: Optional[str]
    trial_condition: Optional[str]
    trial_intent: Optional[str]
    file_summary: Optional[str]
    ai_insights: Optional[str]
    state: Optional[CopilotSessionState]  # This includes the new CopilotSessionState model

    class Config:
        orm_mode = True  # Allows Pydantic to work with ORM models directly
