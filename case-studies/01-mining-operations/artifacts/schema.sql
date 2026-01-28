-- Mining Operations Database Schema
-- Simplified for demonstration

PRAGMA foreign_keys = ON;

-- Equipment master table
CREATE TABLE IF NOT EXISTS equipment_master (
    equipment_id TEXT PRIMARY KEY,
    equipment_name TEXT NOT NULL,
    equipment_type TEXT,
    location_code TEXT,
    status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Equipment sensor readings
CREATE TABLE IF NOT EXISTS equipment_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    reading_value REAL NOT NULL,
    timestamp DATETIME NOT NULL,
    status_code INTEGER NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id)
);

-- Production data
CREATE TABLE IF NOT EXISTS production_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_id TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    material_type TEXT NOT NULL,
    quantity_mined REAL NOT NULL,
    operating_hours REAL NOT NULL,
    record_date DATE NOT NULL,
    efficiency REAL,
    
    FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id)
);

-- Safety compliance
CREATE TABLE IF NOT EXISTS safety_compliance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspection_id TEXT NOT NULL UNIQUE,
    location_code TEXT NOT NULL,
    inspection_date DATE NOT NULL,
    measured_width REAL NOT NULL,
    required_width REAL NOT NULL,
    deviation REAL GENERATED ALWAYS AS (measured_width - required_width),
    compliance_status TEXT GENERATED ALWAYS AS (
        CASE 
            WHEN ABS(measured_width - required_width) <= 0.10 THEN 'COMPLIANT'
            WHEN ABS(measured_width - required_width) <= 0.20 THEN 'MINOR_ISSUE'
            ELSE 'NON_COMPLIANT'
        END
    )
);

-- Sample data
INSERT OR IGNORE INTO equipment_master (equipment_id, equipment_name, equipment_type, location_code) VALUES
('EX001', 'Excavator 001', 'Excavator', 'PIT-A'),
('LHD002', 'LHD 002', 'Load-Haul-Dump', 'PIT-B');

INSERT OR IGNORE INTO production_data (shift_id, equipment_id, material_type, quantity_mined, operating_hours, record_date) VALUES
('SH2024011501', 'EX001', 'Copper Ore', 150.5, 7.5, '2024-01-15');

INSERT OR IGNORE INTO safety_compliance (inspection_id, location_code, inspection_date, measured_width, required_width) VALUES
('INS001', 'PIT-A', '2024-01-15', 4.85, 5.00);
