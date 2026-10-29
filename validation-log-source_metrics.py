```python
import logging

import oracledb
import pymysql

from config.config import get_oracle_config, get_mysql_config

logger = logging.getLogger(__name__)


def get_oracle_metrics():
    """Collect reconciliation metrics directly from Oracle."""
    connection = oracledb.connect(**get_oracle_config())

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_records,
                    COUNT(DISTINCT mf_id) AS unique_meter_ids,
                    COALESCE(SUM(generation_mwh), 0)
                        AS total_generation_mwh
                FROM oracle_meter_factor
            """)

            row = cursor.fetchone()

            return {
                "total_records": row[0],
                "unique_meter_ids": row[1],
                "total_generation_mwh": row[2],
            }

    finally:
        connection.close()


def get_mysql_metrics():
    """Collect reconciliation metrics directly from MySQL."""
    connection = pymysql.connect(**get_mysql_config())

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_records,
                    COUNT(DISTINCT mf_id) AS unique_meter_ids,
                    COALESCE(SUM(generation_mwh), 0)
                        AS total_generation_mwh
                FROM mysql_meter_factor
            """)

            row = cursor.fetchone()

            return {
                "total_records": row[0],
                "unique_meter_ids": row[1],
                "total_generation_mwh": row[2],
            }

    finally:
        connection.close()


def get_all_source_metrics():
    """Return independently collected source-system metrics."""
    logger.info("Collecting Oracle source metrics.")
    oracle_metrics = get_oracle_metrics()

    logger.info("Collecting MySQL source metrics.")
    mysql_metrics = get_mysql_metrics()

    return {
        "ORACLE": oracle_metrics,
        "MYSQL": mysql_metrics,
    }
```
