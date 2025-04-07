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
from backend.utils.logger import log_event
from typing import Optional, List, Dict, Any
from pathlib import Path
import logging
from PyPDF2 import PdfReader
from backend.utils.state_updater import update_session_state
from backend.logic.fivews_initializer import get_5w_context
from backend.db.connection import get_conn
from models.session_state import FileInsight
from .website_scraper import WebsiteScraper
from .aact_connector import AACTConnector
from .document_processor import DocumentProcessor
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_key_findings(text: str) -> List[str]:
    """Extract key findings from document text using rules or ML"""
    # TODO: Implement more sophisticated extraction
    findings = []
    if "objective" in text.lower():
        findings.append("Contains study objective")
    if "inclusion criteria" in text.lower():
        findings.append("Defines inclusion criteria")
    if "exclusion criteria" in text.lower():
        findings.append("Defines exclusion criteria")
    return findings

def integrate_5ws_answers(session_id: int, new_answers: Dict[str, str], filename: str) -> Dict[str, Any]:
    """
    Integrate new 5Ws answers with existing ones, updating confidence levels
    and maintaining supporting document references.
    """
    conn = get_conn()
    cur = conn.cursor()

    try:
        # Get current state
        cur.execute("SELECT state FROM copilot.sessions WHERE id = %s", (session_id,))
        current_state = cur.fetchone()[0]

        integrated = {}
        for key, new_answer in new_answers.items():
            current_answer = current_state.get("fivews", {}).get("answers", {}).get(key, {})

            if not current_answer:
                # First answer for this question
                integrated[key] = {
                    "answer": new_answer,
                    "confidence": 0.7,  # Initial confidence
                    "supporting_files": [filename]
                }
            else:
                # Integrate with existing answer
                if new_answer == current_answer["answer"]:
                    # Corroborating evidence increases confidence
                    integrated[key] = {
                        "answer": current_answer["answer"],
                        "confidence": min(0.95, current_answer["confidence"] + 0.1),
                        "supporting_files": list(set(current_answer["supporting_files"] + [filename]))
                    }
                else:
                    # Conflicting evidence - keep higher confidence answer
                    if current_answer["confidence"] >= 0.7:
                        integrated[key] = current_answer
                    else:
                        integrated[key] = {
                            "answer": new_answer,
                            "confidence": 0.7,
                            "supporting_files": [filename]
                        }

        return integrated

    finally:
        cur.close()
        conn.close()

def run_pipeline(session_id: int, file_path: Path) -> None:
    """
    Process uploaded file and update session state with integrated insights.

    Args:
        session_id: Session to update
        file_path: Path to uploaded file

    Raises:
        ValueError: If file processing fails
        RuntimeError: If state update fails
    """
    logger.info(f"Starting pipeline for session {session_id}")

    try:
        # 1. Extract text and store in uploads table
        preview = ""
        try:
            reader = PdfReader(str(file_path))
            preview = "\n".join([p.extract_text() or "" for p in reader.pages])
            logger.debug("Successfully extracted text from PDF")

            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO copilot.uploads (session_id, file_name, file_path)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (session_id, file_path.name, str(file_path)))
            upload_id = cur.fetchone()[0]
            conn.commit()

            # Create file insight
            findings = extract_key_findings(preview)
            fivews = get_5w_context(preview)

            file_insight = FileInsight(
                upload_id=upload_id,
                file_name=file_path.name,
                preview=preview[:500],
                key_findings={"findings": findings},
                insights={"findings": findings, "fivews": fivews}
            )

            # Store insights
            cur.execute("""
                INSERT INTO copilot.file_insights (upload_id, insights)
                VALUES (%s, %s)
            """, (upload_id, file_insight.insights))
            conn.commit()

        except Exception as e:
            preview = f"(Error extracting preview: {e})"
            logger.error(f"Failed to extract text: {e}")
            raise

        # 2. Extract insights
        findings = extract_key_findings(preview)
        fivews = get_5w_context(preview)

        # 3. Integrate with existing answers
        integrated_answers = integrate_5ws_answers(session_id, fivews, file_path.name)

        # 4. Update session state with integrated insights
        update_session_state(session_id, {
            "enrichment": {
                "status": "complete",
                "latest_file": file_path.name,
                "file_count": "+1",  # Increment existing count
                "latest_insights": file_insight.model_dump()
            },
            "fivews": {
                "answers": integrated_answers,
                "current_stage": "complete"
            }
        })
        logger.info("Successfully updated session state with integrated insights")

    except Exception as e:
        logger.error(f"Pipeline failed for session {session_id}: {e}")
        # Update state with error
        update_session_state(session_id, {
            "enrichment": {
                "status": "error",
                "errors": [str(e)]
            }
        })
        raise RuntimeError(f"Pipeline failed: {str(e)}")


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

class PipelineRunner:
    """Orchestrates the ETL pipeline components."""

    def __init__(self):
        """Initialize pipeline components."""
        logger.info("Initializing ETL pipeline components")
        self.scraper = WebsiteScraper()
        self.aact = AACTConnector()
        self.doc_processor = DocumentProcessor()
        logger.debug("Pipeline components initialized successfully")

    async def run_pipeline(self, document_paths: List[str], website_url: Optional[str] = None, nct_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the complete ETL pipeline.

        Flow:
        1. Document Processing: Extract and parse document content
        2. Website Scraping: Fetch and analyze company website (if URL provided)
        3. AACT Data: Fetch trial data from AACT database (if NCT ID provided)
        4. Enrichment: Extract scientific/statistical/regulatory elements
        5. Mapping: Map enriched data to trial design models
        6. Storage: Persist all data with proper structure
        7. Integration: Combine all sources into final result

        Args:
            document_paths: List of paths to documents to process
            website_url: Optional company website URL to scrape
            nct_id: Optional NCT ID to fetch AACT data

        Returns:
            Dict containing all processed and integrated data

        Raises:
            Exception: If any pipeline stage fails
        """
        logger.info(f"Starting pipeline run with {len(document_paths)} documents")
        logger.debug(f"Input parameters - website_url: {website_url}, nct_id: {nct_id}")
        logger.debug(f"Document paths: {document_paths}")

        pipeline_start = datetime.utcnow()
        stage_times = {}

        try:
            # 1. Document Processing
            stage_start = datetime.utcnow()
            logger.info("Starting document processing phase")
            doc_results = []
            for doc_path in document_paths:
                logger.debug(f"Processing document: {doc_path}")
                try:
                    doc_result = self.doc_processor.process_document(doc_path)
                    logger.debug(f"Document processing result: {doc_result}")
                    logger.debug(f"Document text length: {len(doc_result.get('text', ''))}")
                    logger.debug(f"Document metadata: {doc_result.get('metadata', {})}")
                    doc_results.append(doc_result)
                except Exception as e:
                    logger.error(f"Error processing document {doc_path}: {str(e)}", exc_info=True)
                    raise
            stage_times["document_processing"] = (datetime.utcnow() - stage_start).total_seconds()
            logger.info(f"Document processing completed in {stage_times['document_processing']:.2f}s")

            # 2. Website Scraping (if URL provided)
            stage_start = datetime.utcnow()
            website_data = {}
            if website_url:
                logger.info(f"Starting website scraping for: {website_url}")
                try:
                    website_data = await self.scraper.scrape_website(website_url)
                    logger.debug(f"Website scraping result: {website_data}")
                    logger.debug(f"Website data keys: {list(website_data.keys())}")
                    logger.debug(f"Website content length: {len(website_data.get('content', ''))}")
                except Exception as e:
                    logger.error(f"Error scraping website: {str(e)}", exc_info=True)
                    raise
            stage_times["website_scraping"] = (datetime.utcnow() - stage_start).total_seconds()
            if website_url:
                logger.info(f"Website scraping completed in {stage_times['website_scraping']:.2f}s")

            # 3. AACT Data Enrichment (if NCT ID provided)
            stage_start = datetime.utcnow()
            aact_data = {}
            if nct_id:
                logger.info(f"Fetching AACT data for NCT ID: {nct_id}")
                try:
                    aact_data = self.aact.get_trial_info(nct_id)
                    logger.debug(f"AACT data result: {aact_data}")
                    logger.debug(f"AACT data keys: {list(aact_data.keys())}")
                    logger.debug(f"AACT trial title: {aact_data.get('title', 'N/A')}")
                except Exception as e:
                    logger.error(f"Error fetching AACT data: {str(e)}", exc_info=True)
                    raise
            stage_times["aact_enrichment"] = (datetime.utcnow() - stage_start).total_seconds()
            if nct_id:
                logger.info(f"AACT data fetching completed in {stage_times['aact_enrichment']:.2f}s")

            # 4. Enrichment
            stage_start = datetime.utcnow()
            logger.info("Starting enrichment phase")
            enrichment_results = []
            for doc_result in doc_results:
                logger.debug(f"Enriching document result: {doc_result}")
                try:
                    enriched = enrich_document(doc_result, overrides={})
                    logger.debug(f"Enrichment result: {enriched}")
                    logger.debug(f"Enrichment keys: {list(enriched.keys())}")
                    logger.debug(f"Scientific findings count: {len(enriched.get('scientific', {}).get('findings', []))}")
                    enrichment_results.append(enriched)
                except Exception as e:
                    logger.error(f"Error during enrichment: {str(e)}", exc_info=True)
                    raise
            stage_times["enrichment"] = (datetime.utcnow() - stage_start).total_seconds()
            logger.info(f"Enrichment completed in {stage_times['enrichment']:.2f}s")

            # 5. Mapping
            stage_start = datetime.utcnow()
            logger.info("Starting mapping phase")
            mapped_results = []
            for enriched in enrichment_results:
                logger.debug(f"Mapping enriched result: {enriched}")
                try:
                    mapped = map_to_trial_model(enriched)
                    logger.debug(f"Mapping result: {mapped}")
                    logger.debug(f"Mapping keys: {list(mapped.keys())}")
                    logger.debug(f"Trial design elements: {mapped.get('trial', {}).keys()}")
                    mapped_results.append(mapped)
                except Exception as e:
                    logger.error(f"Error during mapping: {str(e)}", exc_info=True)
                    raise
            stage_times["mapping"] = (datetime.utcnow() - stage_start).total_seconds()
            logger.info(f"Mapping completed in {stage_times['mapping']:.2f}s")

            # 6. Storage
            stage_start = datetime.utcnow()
            logger.info("Starting storage phase")
            try:
                # Prepare data for storage
                parsed_dict = {
                    "raw_text": "\n".join([doc.get("text", "") for doc in doc_results]),
                    "metadata": {
                        "document_count": len(doc_results),
                        "website_url": website_url,
                        "nct_id": nct_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
                logger.debug(f"Parsed dict size: {len(str(parsed_dict))} chars")

                enriched_dict = {
                    "scientific": enrichment_results[0] if enrichment_results else {},
                    "statistical": {},
                    "regulatory": {},
                    "website": website_data,
                    "aact": aact_data
                }
                logger.debug(f"Enriched dict size: {len(str(enriched_dict))} chars")

                mapped_dict = {
                    "trial": mapped_results[0] if mapped_results else {},
                    "population": {},
                    "outcomes": {}
                }
                logger.debug(f"Mapped dict size: {len(str(mapped_dict))} chars")

                storage_result = await store_outputs(
                    parsed=parsed_dict,
                    enriched=enriched_dict,
                    mapped=mapped_dict
                )
                logger.debug(f"Storage result: {storage_result}")
            except Exception as e:
                logger.error(f"Error during storage: {str(e)}", exc_info=True)
                raise
            stage_times["storage"] = (datetime.utcnow() - stage_start).total_seconds()
            logger.info(f"Storage completed in {stage_times['storage']:.2f}s")

            # 7. Final Integration
            stage_start = datetime.utcnow()
            logger.info("Integrating all results")
            final_result = {
                "documents": doc_results,
                "website": website_data,
                "aact": aact_data,
                "enriched": enrichment_results,
                "mapped": mapped_results,
                "timestamp": datetime.utcnow().isoformat(),
                "pipeline_metrics": {
                    "total_time": (datetime.utcnow() - pipeline_start).total_seconds(),
                    "stage_times": stage_times,
                    "document_count": len(doc_results),
                    "has_website_data": bool(website_data),
                    "has_aact_data": bool(aact_data)
                }
            }
            stage_times["integration"] = (datetime.utcnow() - stage_start).total_seconds()

            logger.debug(f"Final integrated result: {final_result}")
            logger.info("Pipeline run completed successfully")
            logger.info(f"Pipeline metrics: Total time: {final_result['pipeline_metrics']['total_time']:.2f}s")
            logger.info("Stage times:")
            for stage, time in stage_times.items():
                logger.info(f"  - {stage}: {time:.2f}s")

            return final_result

        except Exception as e:
            total_time = (datetime.utcnow() - pipeline_start).total_seconds()
            logger.error(f"Pipeline run failed after {total_time:.2f}s: {str(e)}", exc_info=True)
            raise

    async def process_intake_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process intake form data and run appropriate pipeline components.

        Args:
            form_data: Dict containing intake form data

        Returns:
            Dict containing pipeline results
        """
        logger.info("Processing intake form")
        logger.debug(f"Form data: {form_data}")

        website_url = form_data.get("website_url")
        nct_id = form_data.get("nct_id")
        document_paths = form_data.get("document_paths", [])

        # Run pipeline with provided inputs
        results = await self.run_pipeline(
            document_paths=document_paths,
            website_url=website_url,
            nct_id=nct_id
        )

        # Add intake form metadata
        results["intake_form"] = {
            "processed_at": datetime.utcnow().isoformat(),
            "form_data": form_data
        }

        logger.info("Intake form processing completed")
        return results
