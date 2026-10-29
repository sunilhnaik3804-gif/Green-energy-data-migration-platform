### pip install PyMySQL python-dotenv

```python
import os
import logging
import pymysql
from dotenv import load_dotenv

# Load database configuration
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# MySQL database configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv(
        "MYSQL_DATABASE",
        "green_energy_erp"
    ),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.SSCursor
}


def get_mysql_connection():
    """Create MySQL database connection."""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        logging.info("MySQL database connected successfully")
        return connection

    except pymysql.MySQLError:
        logging.exception("MySQL connection failed")
        raise


def extract_mysql(batch_size=1000):
    """Extract meter-factor data from MySQL in batches."""

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
        FROM mysql_meter_factor
        ORDER BY mf_id
    """

    try:
        connection = get_mysql_connection()

        with connection.cursor() as cursor:
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
                    "MySQL batch extracted: %s records",
                    len(records)
                )

                # Process or pass each batch to the next ETL stage
                for record in records:
                    print(record)

        logging.info(
            "MySQL extraction completed. Total records: %s",
            total_records
        )

    except Exception:
        logging.exception("MySQL extraction failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logging.info("MySQL connection closed")


if __name__ == "__main__":
    extract_mysql(batch_size=1000)
```
