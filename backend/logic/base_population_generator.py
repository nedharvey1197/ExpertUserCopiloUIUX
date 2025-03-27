# backend/logic/base_population_generator.py

import numpy as np
import uuid
import json
from datetime import datetime
from typing import Dict, Any
from models.evaluation_bundle import SyntheticPopulationModel
from backend.db.connection import get_conn

GENERATOR_VERSION = "v0.1.0"
GENERATOR_NAME = "base_population_generator"

def generate_base_population(pop_model: SyntheticPopulationModel, population_size: int = 10000) -> str:
    """
    Generate a synthetic population from a defined distribution and persist it to Postgres.
    Returns a unique population ID.
    """
    if pop_model.distribution_type == "normal":
        population = np.random.normal(pop_model.mean, pop_model.std_dev, population_size)
        method = "numpy.normal"
    elif pop_model.distribution_type == "lognormal":
        sigma = pop_model.std_dev
        mu = np.log(pop_model.mean ** 2 / np.sqrt(pop_model.std_dev ** 2 + pop_model.mean ** 2))
        population = np.random.lognormal(mean=mu, sigma=sigma, size=population_size)
        method = "numpy.lognormal"
    else:
        raise ValueError("Unsupported distribution type.")

    metadata = {
        "generator": GENERATOR_NAME,
        "version": GENERATOR_VERSION,
        "method": method,
        "distribution_type": pop_model.distribution_type,
        "parameters": pop_model.dict(),
        "sample_size": population_size,
        "timestamp": datetime.utcnow().isoformat()
    }

    population_id = str(uuid.uuid4())
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO synthetic_populations (id, trial_id, population_data, config, metadata)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            population_id,
            pop_model.population_name or None,
            json.dumps(population.tolist()),
            json.dumps(pop_model.dict()),
            json.dumps(metadata)
        )
    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Generated population with metadata:", json.dumps(metadata, indent=2))
    return population_id


def get_population_by_id(pop_id: str) -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT population_data, config, metadata FROM synthetic_populations WHERE id = %s",
        (pop_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        population_data, config, metadata = row
        return {
            "population": json.loads(population_data),
            "config": json.loads(config),
            "metadata": json.loads(metadata)
        }
    else:
        return {}
