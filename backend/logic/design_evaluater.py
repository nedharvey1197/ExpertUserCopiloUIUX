# backend/logic/design_evaluator.py

from scipy import stats
import numpy as np
from typing import Dict, Any
from backend.utils.logger import log_event

VERSION = "v0.1.0"


def evaluate_trial_design(trial_design: Dict[str, Any]) -> Dict[str, Any]:
    try:
        arms = trial_design.get("arms", [])
        model = trial_design.get("stat_model", {})

        if len(arms) != 2:
            return {"error": "Only two-arm evaluation supported in this version."}

        n1 = arms[0].get("sample_size", 50)
        n2 = arms[1].get("sample_size", 50)
        mu1 = float(arms[0].get("expected_mean", 1.0))
        mu2 = float(arms[1].get("expected_mean", 1.2))
        sd1 = float(arms[0].get("std_dev", 0.4))
        sd2 = float(arms[1].get("std_dev", 0.4))

        alpha = float(model.get("alpha", 0.05))
        power = float(model.get("power", 0.8))

        pooled_sd = np.sqrt((sd1 ** 2 + sd2 ** 2) / 2)
        effect_size = abs(mu1 - mu2) / pooled_sd
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)

        required_n_per_group = 2 * (z_alpha + z_beta) ** 2 / (effect_size ** 2)

        result = {
            "arm_names": [arms[0].get("name"), arms[1].get("name")],
            "mu1": mu1,
            "mu2": mu2,
            "sd1": sd1,
            "sd2": sd2,
            "observed_effect_size": effect_size,
            "required_sample_per_arm": round(required_n_per_group),
            "actual_sample_per_arm": [n1, n2],
            "sufficient_power": n1 >= required_n_per_group and n2 >= required_n_per_group
        }

        log_event(
            event_type="ttest_evaluation",
            trial_id=trial_design.get("trial_id", "unspecified"),
            user_id=None,
            version=VERSION,
            payload=result
        )

        return result

    except Exception as e:
        return {"error": str(e)}