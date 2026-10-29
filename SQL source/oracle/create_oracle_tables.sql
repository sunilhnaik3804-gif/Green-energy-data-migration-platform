-- ==========================================================
-- PROJECT: Green Energy Data Migration Platform
-- DOMAIN: Wind & Solar Energy
-- SOURCE SYSTEM: Oracle ERP
-- PURPOSE: Create Oracle MF source table with sample data
-- ==========================================================

CREATE TABLE oracle_meter_factor (
    mf_id NUMBER(12) PRIMARY KEY,
    plant_id VARCHAR2(50) NOT NULL,
    plant_name VARCHAR2(150),
    energy_type VARCHAR2(20),
    meter_id VARCHAR2(50) NOT NULL,
    meter_factor NUMBER(12,4),
    generation_mwh NUMBER(15,3),
    effective_date DATE,
    location VARCHAR2(150),
    status VARCHAR2(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- INSERT SAMPLE WIND & SOLAR DATA
-- ==========================================================

INSERT ALL

INTO oracle_meter_factor VALUES (
    2001,
    'ORPL001',
    'Karnataka Wind Energy Plant',
    'WIND',
    'ORMTR001',
    1.2500,
    1250.500,
    DATE '2026-01-01',
    'Karnataka',
    'ACTIVE',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)

INTO oracle_meter_factor VALUES (
    2002,
    'ORPL002',
    'Rajasthan Solar Energy Plant',
    'SOLAR',
    'ORMTR002',
    1.1800,
    980.750,
    DATE '2026-01-02',
    'Rajasthan',
    'ACTIVE',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)

INTO oracle_meter_factor VALUES (
    2003,
    'ORPL003',
    'Tamil Nadu Wind Energy Plant',
    'WIND',
    'ORMTR003',
    1.3200,
    1450.250,
    DATE '2026-01-03',
    'Tamil Nadu',
    'ACTIVE',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)

INTO oracle_meter_factor VALUES (
    2004,
    'ORPL004',
    'Gujarat Solar Energy Plant',
    'SOLAR',
    'ORMTR004',
    1.1500,
    1100.600,
    DATE '2026-01-04',
    'Gujarat',
    'ACTIVE',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)

INTO oracle_meter_factor VALUES (
    2005,
    'ORPL005',
    'Maharashtra Wind Energy Plant',
    'WIND',
    'ORMTR005',
    1.2800,
    1320.900,
    DATE '2026-01-05',
    'Maharashtra',
    'INACTIVE',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)

SELECT 1 FROM DUAL;

COMMIT;

-- ==========================================================
-- VALIDATE SOURCE DATA
-- ==========================================================

SELECT COUNT(*) AS total_records
FROM oracle_meter_factor;

SELECT *
FROM oracle_meter_factor
ORDER BY mf_id;
