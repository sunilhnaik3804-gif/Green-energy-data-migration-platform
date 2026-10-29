```python
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from etl.incremental_pipeline import run_incremental_pipeline
from validation.data_quality import validate_staging_data
from validation.reconciliation import (
    get_reconciliation_results,
    reconcile_source_to_target,
)

# --------------------------------------------------
# 1. Create log directory
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("green_energy_orchestrator")


# --------------------------------------------------
# 2. Main orchestration
# --------------------------------------------------

def run_orchestrator():
    run_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info("=" * 60)
    logger.info("GREEN ENERGY ETL PIPELINE STARTED")
    logger.info("Run ID: %s", run_id)
    logger.info(
        "Start time UTC: %s",
        datetime.now(timezone.utc).isoformat(),
    )

    try:
        # Step A: Extract, transform, and load incremental data
        logger.info("STEP A: Starting incremental ETL")

        run_incremental_pipeline()

        logger.info("STEP A: Incremental ETL completed")

        # Step B: Validate staging data
        logger.info("STEP B: Running data quality validation")

        if not validate_staging_data():
            raise RuntimeError("Data quality validation failed")

        logger.info("STEP B: Data quality validation passed")

        # Step C: Reconcile against expected source totals.
        # These totals are captured from staging here; in a full
        # implementation, compare them against independently
        # collected Oracle and MySQL source metrics.
        logger.info("STEP C: Reading staging reconciliation metrics")

        actual_metrics = get_reconciliation_results()

        if not actual_metrics:
            raise RuntimeError(
                "No staging metrics available for reconciliation"
            )

        logger.info(
            "Staging metrics retrieved: %s",
            actual_metrics,
        )

        # Important: staging metrics alone cannot prove source-to-target
        # reconciliation. Expected source metrics must be obtained
        # independently from Oracle and MySQL.
        logger.warning(
            "Independent source metrics are required for true "
            "source-to-target reconciliation."
        )

        elapsed = round(time.time() - start_time, 2)

        logger.info("PIPELINE STATUS: SUCCESS")
        logger.info("Run ID: %s", run_id)
        logger.info("Duration seconds: %s", elapsed)

        return True

    except Exception:
        elapsed = round(time.time() - start_time, 2)

        logger.exception("PIPELINE STATUS: FAILED")
        logger.error("Run ID: %s", run_id)
        logger.error("Duration seconds before failure: %s", elapsed)

        return False

    finally:
        logger.info("GREEN ENERGY ETL PIPELINE FINISHED")
        logger.info("=" * 60)


if __name__ == "__main__":
    success = run_orchestrator()

    if not success:
        sys.exit(1)
```
