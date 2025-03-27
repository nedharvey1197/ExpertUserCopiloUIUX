# backend/models/evaluation_bundle.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- Population Model ---
class SyntheticPopulationModel(BaseModel):
    population_name: Optional[str] = None
    condition_stage: Optional[str] = None
    total_size: int
    mean: float
    std_dev: float
    distribution_type: Literal["normal", "lognormal", "custom"] = "normal"
    notes: Optional[str] = None

# --- Trial Design Arm ---
class TrialArm(BaseModel):
    name: str
    intervention: Optional[str] = None
    sample_size: Optional[int] = None
    expected_mean: Optional[float] = None
    std_dev: Optional[float] = None
    allocation_ratio: Optional[float] = 0.5

# --- Statistical Evaluation Configuration ---
class StatisticalEvaluationConfig(BaseModel):
    test_type: Literal["t-test", "wilcoxon", "bootstrap", "bayesian"] = "t-test"
    alpha: float = 0.05
    power: float = 0.8
    ci_method: Literal["formula", "bootstrap"] = "formula"
    simulate_from_population: bool = True
    num_simulations: int = 1000
    assumption_checking: bool = True
    include_visuals: bool = False

# --- Trial Design Container ---
class TrialDesignEvaluation(BaseModel):
    sponsor: Optional[str]
    trial_id: Optional[str]
    phase: Literal["1", "1/2", "2", "2/3", "3", "4"]
    indication: str
    population_description: str
    therapeutic_area: Optional[str]
    design: Literal["parallel", "crossover", "adaptive"]
    arms: List[TrialArm]
    population_model: SyntheticPopulationModel
    evaluation_config: StatisticalEvaluationConfig