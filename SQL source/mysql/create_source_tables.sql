-- ==========================================================
-- PROJECT: Green Energy Data Migration Platform
-- DOMAIN: Wind & Solar Energy
-- SOURCE SYSTEM: MySQL
-- PURPOSE: Create MySQL MF source table with sample data
-- ==========================================================

CREATE DATABASE IF NOT EXISTS green_energy_erp;

USE green_energy_erp;

-- ==========================================================
-- CREATE SOURCE TABLE
-- ==========================================================

CREATE TABLE IF NOT EXISTS mysql_meter_factor (

    mf_id BIGINT PRIMARY KEY,

    plant_id VARCHAR(50) NOT NULL,

    plant_name VARCHAR(150),

    energy_type VARCHAR(20),

    meter_id VARCHAR(50) NOT NULL,

    meter_factor DECIMAL(12,4),

    generation_mwh DECIMAL(15,3),

    effective_date DATE,

    location VARCHAR(150),

    status VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);

-- ==========================================================
-- INSERT SAMPLE WIND & SOLAR DATA
-- ==========================================================

INSERT INTO mysql_meter_factor
(
    mf_id,
    plant_id,
    plant_name,
    energy_type,
    meter_id,
    meter_factor,
    generation_mwh,
    effective_date,
    location,
    status
)
VALUES

(
    1001,
    'MYPL001',
    'Karnataka Wind Farm',
    'WIND',
    'MYMTR001',
    1.2500,
    1200.500,
    '2026-01-01',
    'Karnataka',
    'ACTIVE'
),

(
    1002,
    'MYPL002',
    'Rajasthan Solar Plant',
    'SOLAR',
    'MYMTR002',
    1.1800,
    950.750,
    '2026-01-02',
    'Rajasthan',
    'ACTIVE'
),

(
    1003,
    'MYPL003',
    'Tamil Nadu Wind Farm',
    'WIND',
    'MYMTR003',
    1.3200,
    1400.250,
    '2026-01-03',
    'Tamil Nadu',
    'ACTIVE'
),

(
    1004,
    'MYPL004',
    'Gujarat Solar Plant',
    'SOLAR',
    'MYMTR004',
    1.1500,
    1080.600,
    '2026-01-04',
    'Gujarat',
    'ACTIVE'
),

(
    1005,
    'MYPL005',
    'Maharashtra Wind Farm',
    'WIND',
    'MYMTR005',
    1.2800,
    1300.900,
    '2026-01-05',
    'Maharashtra',
    'INACTIVE'
)

ON DUPLICATE KEY UPDATE
    plant_id = VALUES(plant_id),
    plant_name = VALUES(plant_name),
    energy_type = VALUES(energy_type),
    meter_id = VALUES(meter_id),
    meter_factor = VALUES(meter_factor),
    generation_mwh = VALUES(generation_mwh),
    effective_date = VALUES(effective_date),
    location = VALUES(location),
    status = VALUES(status);

-- ==========================================================
-- VALIDATE SOURCE DATA
-- ==========================================================

SELECT COUNT(*) AS total_records
FROM mysql_meter_factor;

SELECT *
FROM mysql_meter_factor
ORDER BY mf_id;
