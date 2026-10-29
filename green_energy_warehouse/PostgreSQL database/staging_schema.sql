```sql
-- Green Energy Data Migration Platform
-- Step 6: PostgreSQL staging table

CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.meter_factor_staging (
    source_system VARCHAR(20) NOT NULL,
    mf_id BIGINT NOT NULL,

    plant_id VARCHAR(50) NOT NULL,
    plant_name VARCHAR(150),
    energy_type VARCHAR(20),
    meter_id VARCHAR(50) NOT NULL,

    meter_factor NUMERIC(12,4),
    generation_mwh NUMERIC(15,3),
    effective_date DATE,

    location VARCHAR(150),
    status VARCHAR(20),

    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,

    batch_id VARCHAR(100) NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_meter_factor_staging
        PRIMARY KEY (source_system, mf_id)
);
```


---------------------------------------------------------------------
#### Validate the staging table
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'staging'
  AND table_name = 'meter_factor_staging'
ORDER BY ordinal_position;
-----------------------------------------------------------------------
#####current record count:
SELECT COUNT(*) AS total_records
FROM staging.meter_factor_staging;

python -m pip install -r requirements.txt
