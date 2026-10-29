# Green-energy-data-migration-platform
End-to-end Green Energy Data Migration project using Python, SQL, Apache Airflow, Oracle ERP, MySQL, Informix staging, PostgreSQL and Power BI. Includes ETL pipelines, incremental loading, data validation, reconciliation and monitoring.


# Green Energy Data Migration Platform

## Project Overview

This project implements a Python-based ETL pipeline that migrates renewable-energy meter-factor data from Oracle and MySQL into PostgreSQL.

The pipeline extracts source records, transforms and validates the data, loads it into PostgreSQL staging, tracks incremental changes using update timestamps, and performs data quality checks and source-to-target reconciliation.

## Business Objective

Consolidate meter-factor and energy-generation records from multiple source databases into a PostgreSQL staging environment while improving data consistency, traceability, and migration reliability.

## Technology Stack

* Python
* Oracle Database
* MySQL
* PostgreSQL
* SQL
* Pandas
* Psycopg2
* Python dotenv
* Logging
* Git and GitHub

## Architecture

Oracle Database ──┐
├──> Python Extraction
MySQL Database ───┘
|
v
Incremental Processing
|
v
Data Transformation
|
v
PostgreSQL Staging
|
v
Data Quality Checks
|
v
Source-Target Reconciliation
|
v
Execution Logs

## Source Systems

### Oracle

Source table: `oracle_meter_factor`

### MySQL

Source table: `mysql_meter_factor`

Both tables contain meter-factor and renewable-energy generation information.

Important columns include:

* `mf_id`
* `plant_id`
* `plant_name`
* `energy_type`
* `meter_id`
* `meter_factor`
* `generation_mwh`
* `effective_date`
* `location`
* `status`
* `created_at`
* `updated_at`

## Target System

Database: `green_energy_warehouse`

Staging table: `staging.meter_factor_staging`

Watermark table: `public.etl_watermarks`

The staging table stores source-system identifiers and batch metadata to support traceability and idempotent upserts.

## ETL Workflow

1. Connect to Oracle and MySQL.
2. Extract meter-factor records.
3. Identify new or updated records using source update timestamps.
4. Standardize data types and values.
5. Validate mandatory fields and business rules.
6. Load records into PostgreSQL staging.
7. Track source-system watermarks.
8. Run staging data quality checks.
9. Compare source metrics with target metrics.
10. Log pipeline execution and failures.

## Data Quality Rules

The pipeline checks for:

* Missing required fields
* Duplicate source identifiers
* Invalid energy types
* Meter factors outside the configured range
* Negative or missing generation values
* Missing update timestamps

## Incremental Loading

The pipeline uses `updated_at` timestamps and a PostgreSQL watermark table to track incremental processing.

The loader uses conflict handling on `(source_system, mf_id)` so repeated processing can update an existing staging record rather than create a duplicate.

Production deployment should additionally implement fixed run boundaries, timestamp overlap handling, recovery-safe watermark advancement, and an explicit initial-load strategy.

## Reconciliation

The reconciliation component compares source-system metrics with PostgreSQL staging metrics.

Metrics include:

* Total records
* Unique meter-factor IDs
* Total generation in MWh

The comparison must use consistent source snapshots and account for rejected records and incremental processing scope.

## Configuration

Create a local `.env` file containing the connection settings required by the application.

Use `.env.example` to document the required variable names without including actual credentials.

Never commit passwords, database credentials, or other secrets to GitHub.

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the orchestrator:

```bash
python -m etl.orchestrator
```

Run data quality validation:

```bash
python -m validation.data_quality
```

Run reconciliation:

```bash
python -m validation.reconciliation
```

Run commands from the repository root with the virtual environment activated.

## Logging

The orchestrator records execution events, errors, run identifiers, and execution duration.

Runtime logs are stored locally in the `logs/` directory, which should be excluded from version control.

## Future Improvements

* Apache Airflow DAG scheduling
* Automated unit and integration tests
* Retry handling and alert notifications
* Rejected-record storage
* Transaction-safe watermark management
* Containerized deployment
* CI/CD automation
* Production-grade metrics and monitoring

## Disclaimer

This is a portfolio and learning project. Validate database connections, schema compatibility, transaction handling, and incremental-load correctness before using the implementation in a production environment.

