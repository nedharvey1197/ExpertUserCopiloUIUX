# backend/models/trial_design.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Arm(BaseModel):
    name: str
    description: Optional[str] = None
    sample_size: Optional[int] = None
    intervention: Optional[str] = None

class Endpoint(BaseModel):
    name: str
    type: Literal["primary", "secondary", "exploratory"]
    description: Optional[str] = None

class StatModelConfig(BaseModel):
    model_type: Literal[
        "binomial", "cox", "linear", "logistic", "bayesian-binomial", "simon-two-stage"
    ]
    expected_effect_size: Optional[float] = None
    alpha: Optional[float] = Field(default=0.05)
    power: Optional[float] = Field(default=0.8)
    dropout_rate: Optional[float] = Field(default=0.1)
    hazard_ratio: Optional[float] = None
    notes: Optional[str] = None
    
class StatEvaluationPlan(BaseModel):
    test_type: Literal["t-test", "wilcoxon", "bootstrap", "simulation"]
    hypothesis_null: Optional[str] = None  # e.g., "μ = 51"
    hypothesis_alt: Optional[str] = None   # e.g., "μ ≠ 51"
    simulate_data: bool = False
    simulate_n_samples: Optional[int] = 1000
    ci_method: Literal["formula", "bootstrap"] = "formula"
    alpha: float = 0.05
    output_required: List[Literal["p-value", "ci", "distribution", "explanation"]]

class TrialDesign(BaseModel):
    sponsor: Optional[str] = None
    trial_id: Optional[str] = None
    title: Optional[str] = None
    phase: Literal["1", "1/2", "2", "2/3", "3", "4"]
    indication: str
    population: str
    randomization: Literal["none", "1:1", "2:1", "stratified"]
    blinding: Optional[Literal["open-label", "single", "double"]] = None
    sample_size: int
    intervention: str
    control: Optional[str] = None
    arms: List[Arm]
    endpoints: List[Endpoint]
    stat_model: StatModelConfig
    location: Optional[str] = None
    duration_months: Optional[int] = None
    synopsis: Optional[str] = None
