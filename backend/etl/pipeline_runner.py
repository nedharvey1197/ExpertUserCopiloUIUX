# 📁 etl/

# ├── __init__.py
# ├── pipeline_runner.py          # Main entrypoint for pipeline execution
# ├── parser_loader.py            # Dynamically loads/parses with selected parser backend
# ├── enrichment_engine.py        # Runs scientific/statistical/regulatory extractors
# ├── mapping_engine.py           # Maps enrichment results → trial schema models
# ├── storage_manager.py          # Handles storage into Postgres/Neo4j/Vector/DeltaLake
# ├── async_tasks.py              # Async enrichment microservices (Celery-ready)
# ├── utils/
# │   ├── logger.py               # Logger used across pipeline
# │   └── file_utils.py           # File, UUID, MIME type, and path handling
# └── configs/
#     ├── pipeline_config.yaml    # Default control flow config
#     └── default_schemas/        # Standard schemas (scientific, regulatory, etc.)

# ---------------------------
# pipeline_runner.py (Stub)
# ----------------------
# # ---------------------------
# pipeline_runner.py (Stub)
# ---------------------------

from .parser_loader import load_parser
from .enrichment_engine import enrich_document
from .mapping_engine import map_to_trial_model
from .storage_manager import store_outputs
from .utils.logger import log_event


def run_pipeline(doc_path: str, config_path: str = None, overrides: dict = {}):
    log_event("PIPELINE_START", {"doc_path": doc_path})

    parsed = load_parser(doc_path, overrides)
    enrichment = enrich_document(parsed, overrides)
    mapped = map_to_trial_model(enrichment)

    store_outputs(parsed, enrichment, mapped)
    log_event("PIPELINE_END", {"status": "complete"})

    return mapped


# === V0 Progress Priorities ===
# 1. Wire `run_pipeline()` into the `/copilot/upload_file` FastAPI route
# 2. Prepare a sample `pipeline_config.yaml` with scientific/statistical defaults
# 3. [Deferred for pipeline backlog]: Implement override mechanism via API params or schema registry reference


# === Next-Upgraded Version: upload_file route ===
# Integrates: file saving, preview parsing, pipeline run, logging, and DB insert

# @router.post("/upload_file") ← In copilot.py
# Inputs: session_id, company_name, company_website, nct_id, file
# Outputs: session_id, parsed preview, enrichment summary, message

# ✅ Logging and provenance supported via etl.logger
# ✅ Future-ready: can extend to async, background runs, or compliance retention

