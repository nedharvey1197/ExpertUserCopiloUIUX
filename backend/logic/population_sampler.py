# backend/logic/population_sampler.py

import numpy as np
from typing import List, Dict
from models.evaluation_bundle import SyntheticPopulationModel, TrialArm
from backend.utils.logger import log_event

VERSION = "v0.1.0"


def sample_population(pop: SyntheticPopulationModel, sample_size: int) -> np.ndarray:
    if pop.distribution_type == "normal":
        data = np.random.normal(loc=pop.mean, scale=pop.std_dev, size=sample_size)
        method = "numpy.normal"
    elif pop.distribution_type == "lognormal":
        sigma = pop.std_dev
        mu = np.log(pop.mean ** 2 / np.sqrt(pop.std_dev ** 2 + pop.mean ** 2))
        data = np.random.lognormal(mean=mu, sigma=sigma, size=sample_size)
        method = "numpy.lognormal"
    else:
        raise ValueError("Unsupported distribution type.")

    log_event(
        event_type="population_sample",
        trial_id=pop.population_name or "unspecified",
        user_id=None,
        version=VERSION,
        payload={
            "distribution": pop.distribution_type,
            "method": method,
            "sample_size": sample_size,
            "parameters": pop.dict()
        }
    )
    return data


def generate_arm_samples(pop_model: SyntheticPopulationModel, arms: List[TrialArm]) -> Dict[str, List[float]]:
    sampled_data = {}
    for arm in arms:
        n = arm.sample_size or int(pop_model.total_size / len(arms))
        data = sample_population(pop_model, n)
        sampled_data[arm.name] = data.tolist()
    return sampled_data


def summarize_samples(sample_dict: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
    return {
        name: {
            "n": len(values),
            "mean": float(np.mean(values)),
            "std_dev": float(np.std(values, ddof=1)),
            "min": float(np.min(values)),
            "max": float(np.max(values))
        }
        for name, values in sample_dict.items()
    }