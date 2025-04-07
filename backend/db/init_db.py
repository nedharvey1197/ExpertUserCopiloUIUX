"""Database initialization script."""
import logging
from pathlib import Path
from backend.db.connection import get_conn

logger = logging.getLogger(__name__)

def init_db():
    """Initialize database schema."""
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Read and execute SQL script
        sql_path = Path(__file__).parent / 'init_db.sql'
        with open(sql_path, 'r') as f:
            sql = f.read()

        logger.info("Initializing database schema...")
        cur.execute(sql)
        conn.commit()
        logger.info("Database schema initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    init_db()
