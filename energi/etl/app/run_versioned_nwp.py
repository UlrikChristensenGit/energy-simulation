import dotenv
from pathlib import Path

dotenv.load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from logs import get_logger

logger = get_logger(__name__)

from jobs.versioned_nwp.job import VersionedNwpETL

if __name__ == "__main__":
    try:
        etl = VersionedNwpETL()

        etl.run()
    except Exception:
        logger.exception("Error occurred during ETL run")
