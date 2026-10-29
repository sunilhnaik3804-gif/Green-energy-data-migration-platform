
CREATE TABLE stg_meter_factor (

    staging_id SERIAL PRIMARY KEY,

    source_system VARCHAR(20) NOT NULL,

    source_mf_id BIGINT NOT NULL,

    plant_id VARCHAR(50),

    plant_name VARCHAR(150),

    energy_type VARCHAR(20),

    meter_id VARCHAR(50),

    meter_factor DECIMAL(12,4),

    generation_mwh DECIMAL(15,3),

    effective_date DATE,

    location VARCHAR(150),

    status VARCHAR(20),

    source_created_at DATETIME YEAR TO FRACTION(5),

    source_updated_at DATETIME YEAR TO FRACTION(5),

    migration_batch_id VARCHAR(50),

    ingestion_timestamp DATETIME YEAR TO SECOND
        DEFAULT CURRENT YEAR TO SECOND

);


=====================================================
-- CREATE INDEXES
-- =====================================================

CREATE UNIQUE INDEX idx_stg_source_mf
ON stg_meter_factor (
    source_system,
    source_mf_id
);

CREATE INDEX idx_stg_batch
ON stg_meter_factor (
    migration_batch_id



-- =====================================================
-- VALIDATION QUERIES
-- =====================================================

-- Total staging records
SELECT COUNT(*) AS total_records
FROM stg_meter_factor;

-- Oracle source records
SELECT COUNT(*) AS oracle_records
FROM stg_meter_factor
WHERE source_system = 'ORACLE';

-- MySQL source records
SELECT COUNT(*) AS mysql_records
FROM stg_meter_factor
WHERE source_system = 'MYSQL';

-- View staging data
SELECT *
FROM stg_meter_factor;
