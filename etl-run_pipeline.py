```python
import logging
from uuid import uuid4

from etl.extract import extract_oracle, extract_mysql
from etl.transform import transform_meter_factor
from etl.load import load_staging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def process_source(source_name, extraction_function, batch_id):
    """Extract, transform, validate, and load one source."""

    total_extracted = 0
    total_valid = 0
    total_invalid = 0
    batch_number = 0

    logging.info("Starting %s pipeline", source_name)

    for extracted_batch in extraction_function(batch_size=1000):
        batch_number += 1
        total_extracted += len(extracted_batch)

        logging.info(
            "%s: processing batch %s with %s records",
            source_name,
            batch_number,
            len(extracted_batch),
        )

        valid_records, invalid_records = transform_meter_factor(
            extracted_batch,
            source_name,
        )

        total_valid += len(valid_records)
        total_invalid += len(invalid_records)

        # Stop the pipeline if any record fails validation.
        # A later step will implement persistent error storage.
        if not invalid_records.empty:
            logging.error(
                "%s: %s invalid records found in batch %s",
                source_name,
                len(invalid_records),
                batch_number,
            )

            raise ValueError(
                f"{source_name}: invalid records detected. "
                "Pipeline stopped before loading this batch."
            )

        if not valid_records.empty:
            records = valid_records.to_dict(orient="records")

            load_staging(
                records=records,
                source_system=source_name,
                batch_id=batch_id,
            )

    logging.info(
        "%s completed: extracted=%s, valid=%s, invalid=%s",
        source_name,
        total_extracted,
        total_valid,
        total_invalid,
    )

    return {
        "source": source_name,
        "extracted": total_extracted,
        "valid": total_valid,
        "invalid": total_invalid,
    }


def run_pipeline():
    """Execute the Oracle and MySQL migration pipeline."""

    batch_id = str(uuid4())

    logging.info("=" * 60)
    logging.info("GREEN ENERGY DATA MIGRATION STARTED")
    logging.info("Batch ID: %s", batch_id)
    logging.info("=" * 60)

    results = []

    sources = [
        ("ORACLE", extract_oracle),
        ("MYSQL", extract_mysql),
    ]

    for source_name, extraction_function in sources:
        result = process_source(
            source_name=source_name,
            extraction_function=extraction_function,
            batch_id=batch_id,
        )

        results.append(result)

    logging.info("=" * 60)
    logging.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
    logging.info("Batch ID: %s", batch_id)

    for result in results:
        logging.info(
            "%s | Extracted: %s | Valid: %s | Invalid: %s",
            result["source"],
            result["extracted"],
            result["valid"],
            result["invalid"],
        )

    logging.info("=" * 60)


if __name__ == "__main__":
    try:
        run_pipeline()

    except Exception:
        logging.exception("ETL pipeline failed")
        raise
```
