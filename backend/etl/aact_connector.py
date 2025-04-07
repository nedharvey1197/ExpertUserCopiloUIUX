"""
AACT Database connector for fetching clinical trial information.
Connects to local PostgreSQL database and queries the ctgov schema.
"""
import logging
from typing import Dict, Any, Optional, TypedDict
from datetime import datetime
from backend.db.connection import get_conn

logger = logging.getLogger(__name__)

class DBParams(TypedDict):
    dbname: str
    user: str
    password: str
    host: str
    port: str

class AACTConnector:
    """Connects to and queries the AACT clinical trials data from local ctgov schema."""

    def __init__(self, connection_params: Optional[DBParams] = None):
        """
        Initialize AACT connector.

        Args:
            connection_params: Optional override for AACT connection parameters
        """
        self.conn_params: DBParams = connection_params or {
            'dbname': 'aact',
            'user': 'your_username',  # TODO: Move to env
            'password': 'your_password',  # TODO: Move to env
            'host': 'aact-db.ctti-clinicaltrials.org',
            'port': '5432'
        }

    def get_trial_info(self, nct_id: str) -> Dict[str, Any]:
        """
        Fetch comprehensive trial information from local ctgov schema.

        Args:
            nct_id: The NCT identifier

        Returns:
            Dict containing trial information
        """
        try:
            conn = get_conn()  # Use local database connection
            cur = conn.cursor()

            # Fetch basic trial info
            cur.execute("""
                SELECT
                    s.brief_title,
                    s.official_title,
                    s.phase,
                    s.overall_status,
                    s.why_stopped,
                    s.brief_summary,
                    s.detailed_description,
                    s.study_type,
                    s.study_design,
                    e.criteria
                FROM ctgov.studies s
                LEFT JOIN ctgov.eligibilities e ON e.nct_id = s.nct_id
                WHERE s.nct_id = %s
            """, (nct_id,))

            result = cur.fetchone()
            if not result:
                raise ValueError(f"Trial {nct_id} not found in ctgov schema")

            # Structure basic info
            info = {
                "nct_id": nct_id,
                "brief_title": result[0],
                "official_title": result[1],
                "phase": result[2],
                "status": result[3],
                "why_stopped": result[4],
                "brief_summary": result[5],
                "detailed_description": result[6],
                "study_type": result[7],
                "study_design": result[8],
                "eligibility_criteria": result[9],
                "fetched_at": datetime.utcnow().isoformat()
            }

            # Fetch design details
            cur.execute("""
                SELECT
                    design_group_type,
                    group_label,
                    description
                FROM ctgov.design_groups
                WHERE nct_id = %s
            """, (nct_id,))

            info["design_groups"] = [
                {
                    "type": row[0],
                    "label": row[1],
                    "description": row[2]
                }
                for row in cur.fetchall()
            ]

            # Fetch outcomes
            cur.execute("""
                SELECT
                    outcome_type,
                    measure,
                    time_frame,
                    description
                FROM ctgov.outcomes
                WHERE nct_id = %s
            """, (nct_id,))

            info["outcomes"] = [
                {
                    "type": row[0],
                    "measure": row[1],
                    "time_frame": row[2],
                    "description": row[3]
                }
                for row in cur.fetchall()
            ]

            return info

        except Exception as e:
            logger.error(f"Error fetching trial {nct_id} from ctgov schema: {str(e)}")
            raise

        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    def enrich_trial_data(self, nct_id: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich existing trial data with AACT information.

        Args:
            nct_id: The NCT identifier
            current_data: Current trial information to enrich

        Returns:
            Dict containing merged trial information
        """
        try:
            aact_data = self.get_trial_info(nct_id)

            # Merge data, preferring current data over AACT when available
            enriched = {
                **aact_data,
                **current_data,
                "sources": {
                    "aact": {
                        "fetched_at": aact_data["fetched_at"],
                        "available": True
                    }
                }
            }

            return enriched

        except Exception as e:
            logger.error(f"Failed to enrich trial data for {nct_id}: {str(e)}")
            return {
                **current_data,
                "sources": {
                    "aact": {
                        "fetched_at": datetime.utcnow().isoformat(),
                        "available": False,
                        "error": str(e)
                    }
                }
            }
