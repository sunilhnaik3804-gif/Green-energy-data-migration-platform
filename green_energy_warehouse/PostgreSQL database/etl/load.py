```python
import os
import logging
from uuid import uuid4

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "dbname": os.getenv(
        "POSTGRES_DATABASE",
        "green_energy_warehouse",
    ),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def get_postgres_connection():
    """Connect to PostgreSQL."""

    try:
        connection = psycopg2.connect(**POSTGRES_CONFIG)
        logging.info("PostgreSQL connected successfully")
        return connection

    except psycopg2.Error:
        logging.exception("PostgreSQL connection failed")
        raise


def load_staging(records, source_system, batch_id=None):
    """
    Load transformed records into PostgreSQL staging.

    records: iterable of dictionaries returned by transform.py
    source_system: ORACLE or MYSQL
    batch_id: optional ID shared by records in one ETL batch
    """

    if not records:
        logging.info("No records to load for %s", source_system)
        return 0

    source_system = source_system.upper()

    if source_system not in {"ORACLE", "MYSQL"}:
        raise ValueError("source_system must be ORACLE or MYSQL")

    batch_id = batch_id or str(uuid4())

    columns = [
        "source_system",
        "mf_id",
        "plant_id",
        "plant_name",
        "energy_type",
        "meter_id",
        "meter_factor",
        "generation_mwh",
        "effective_date",
        "location",
        "status",
        "created_at",
        "updated_at",
        "batch_id",
    ]

    values = []

    for record in records:
        values.append(
            (
                source_system,
                int(record["mf_id"]),
                record["plant_id"],
                record.get("plant_name"),
                record.get("energy_type"),
                record["meter_id"],
                record.get("meter_factor"),
                record.get("generation_mwh"),
                record.get("effective_date"),
                record.get("location"),
                record.get("status"),
                record.get("created_at"),
                record.get("updated_at"),
                batch_id,
            )
        )

    query = """
        INSERT INTO staging.meter_factor_staging (
            source_system,
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
            updated_at,
            batch_id
        )
        VALUES %s
        ON CONFLICT (source_system, mf_id)
        DO UPDATE SET
            plant_id = EXCLUDED.plant_id,
            plant_name = EXCLUDED.plant_name,
            energy_type = EXCLUDED.energy_type,
            meter_id = EXCLUDED.meter_id,
            meter_factor = EXCLUDED.meter_factor,
            generation_mwh = EXCLUDED.generation_mwh,
            effective_date = EXCLUDED.effective_date,
            location = EXCLUDED.location,
            status = EXCLUDED.status,
            created_at = EXCLUDED.created_at,
            updated_at = EXCLUDED.updated_at,
            batch_id = EXCLUDED.batch_id,
            loaded_at = CURRENT_TIMESTAMP
    """

    connection = None

    try:
        connection = get_postgres_connection()

        with connection:
            with connection.cursor() as cursor:
                execute_values(
                    cursor,
                    query,
                    values,
                    page_size=1000,
                )

                logging.info(
                    "Loaded %s records from %s. Batch ID: %s",
                    len(values),
                    source_system,
                    batch_id,
                )

        return len(values)

    except Exception:
        logging.exception("Staging load failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logging.info("PostgreSQL connection closed")


if __name__ == "__main__":
    # Test with one record before connecting the full ETL pipeline.
    sample_records = [
        {
            "mf_id": 1001,
            "plant_id": "PLANT001",
            "plant_name": "Solar Plant Bengaluru",
            "energy_type": "SOLAR",
            "meter_id": "MTR001",
            "meter_factor": 0.9850,
            "generation_mwh": 1250.500,
            "effective_date": "2026-10-01",
            "location": "Bengaluru",
            "status": "ACTIVE",
            "created_at": None,
            "updated_at": None,
        }
    ]

    load_staging(sample_records, "ORACLE")
```
