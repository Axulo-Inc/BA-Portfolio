# Data Dictionary
## Mining Operations Dashboard

### Data Sources
1. **IoT Sensor Data** - Equipment temperature, vibration, pressure
2. **ERP System** - Production output, shift data
3. **Maintenance System** - Work orders, downtime tracking
4. **Safety System** - Compliance inspections, stope measurements

### Core Tables

#### equipment_master
| Field | Type | Description |
|-------|------|-------------|
| equipment_id | TEXT | Unique equipment identifier |
| equipment_name | TEXT | Equipment display name |
| equipment_type | TEXT | Type of equipment |
| location_code | TEXT | Current location in mine |
| status | TEXT | Current status (ACTIVE/INACTIVE) |

#### equipment_readings
| Field | Type | Description |
|-------|------|-------------|
| equipment_id | TEXT | Equipment identifier |
| sensor_type | TEXT | Temperature, Vibration, Pressure |
| reading_value | REAL | Sensor measurement |
| timestamp | DATETIME | Time of measurement |
| status_code | INTEGER | 1=Normal, 2=Warning, 3=Critical |

#### production_data
| Field | Type | Description |
|-------|------|-------------|
| shift_id | TEXT | Production shift identifier |
| equipment_id | TEXT | Equipment used |
| material_type | TEXT | Type of material mined |
| quantity_mined | REAL | Tons extracted |
| operating_hours | REAL | Equipment runtime |
| efficiency | REAL | Tons per hour (calculated) |

#### safety_compliance
| Field | Type | Description |
|-------|------|-------------|
| inspection_id | TEXT | Safety inspection identifier |
| location_code | TEXT | Mine section or stope |
| measured_width | REAL | Actual stope width |
| required_width | REAL | Regulatory requirement |
| compliance_status | TEXT | Compliant/Minor Issue/Non-Compliant |

### Key Performance Indicators (KPIs)
1. **OEE** (Overall Equipment Effectiveness) = Availability × Performance × Quality
2. **MTBF** (Mean Time Between Failures) = Total Operating Time ÷ Number of Failures
3. **Compliance Rate** = (Compliant Inspections ÷ Total Inspections) × 100
