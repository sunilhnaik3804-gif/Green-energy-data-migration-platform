### pip install oracledb python-dotenv

```python
import os
import logging
import oracledb
from dotenv import load_dotenv

# Load database configuration
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Oracle database configuration
ORACLE_CONFIG = {
    "user": os.getenv("ORACLE_USER"),
    "password": os.getenv("ORACLE_PASSWORD"),
    "dsn": os.getenv("ORACLE_DSN")
}


def get_oracle_connection():
    """Create Oracle database connection."""
    try:
        connection = oracledb.connect(**ORACLE_CONFIG)
        logging.info("Oracle database connected successfully")
        return connection

    except oracledb.Error:
        logging.exception("Oracle connection failed")
        raise


def extract_oracle(batch_size=1000):
    """Extract meter-factor data from Oracle in batches."""

    connection = None
    total_records = 0

    query = """
        SELECT
            mf_id,
            plant_id,
            plant_name,
            energy_type,
            meter_id,
            meter_factor,
            generation_mwh,
            effective_date,
            location,
            status,
            created_at,
            updated_at
        FROM oracle_meter_factor
        ORDER BY mf_id
    """

    try:
        connection = get_oracle_connection()

        with connection.cursor() as cursor:
            cursor.arraysize = batch_size
            cursor.execute(query)

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            while True:
                rows = cursor.fetchmany(batch_size)

                if not rows:
                    break

                records = [
                    dict(zip(columns, row))
                    for row in rows
                ]

                total_records += len(records)

                logging.info(
                    "Oracle batch extracted: %s records",
                    len(records)
                )

                # Process or pass each batch to the next ETL stage
                for record in records:
                    print(record)

        logging.info(
            "Oracle extraction completed. Total records: %s",
            total_records
        )

    except Exception:
        logging.exception("Oracle extraction failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logging.info("Oracle connection closed")


if __name__ == "__main__":
    extract_oracle(batch_size=1000)
```
