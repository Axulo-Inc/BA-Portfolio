#!/usr/bin/env python3
"""
Mining Operations ETL Pipeline - Simplified Version
Purpose: Extract, Transform, Load mining data for dashboard
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MiningETLPipeline:
    def __init__(self, db_path="mining_data.db"):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create equipment readings table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment_readings (
            id INTEGER PRIMARY KEY,
            equipment_id TEXT NOT NULL,
            sensor_type TEXT,
            reading_value REAL,
            timestamp DATETIME,
            status INTEGER
        )
        ''')
        
        # Create production data table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS production_data (
            id INTEGER PRIMARY KEY,
            shift_id TEXT,
            equipment_id TEXT,
            quantity_mined REAL,
            operating_hours REAL,
            record_date DATE
        )
        ''')
        
        self.conn.commit()
        logger.info("Database initialized")
    
    def extract_sample_data(self):
        """Extract sample data for demonstration"""
        logger.info("Extracting sample data...")
        
        # Sample equipment readings
        equipment_data = [
            {"equipment_id": "EX001", "sensor_type": "temperature", "reading_value": 75.5, "timestamp": "2024-01-15 08:30:00"},
            {"equipment_id": "EX001", "sensor_type": "vibration", "reading_value": 2.3, "timestamp": "2024-01-15 08:30:00"},
        ]
        
        # Sample production data
        production_data = [
            {"shift_id": "SH2024011501", "equipment_id": "EX001", "quantity_mined": 150.5, "operating_hours": 7.5},
        ]
        
        return equipment_data, production_data
    
    def transform_data(self, raw_data, data_type):
        """Transform data with business rules"""
        transformed = []
        
        for record in raw_data:
            if data_type == "equipment":
                # Add status based on sensor readings
                record["status"] = self.calculate_status(record)
                transformed.append(record)
        
        logger.info(f"Transformed {len(transformed)} {data_type} records")
        return transformed
    
    def calculate_status(self, record):
        """Calculate equipment status"""
        if record["sensor_type"] == "temperature":
            if record["reading_value"] > 100:
                return 3  # Critical
            elif record["reading_value"] > 85:
                return 2  # Warning
            else:
                return 1  # Normal
        return 1
    
    def load_data(self, data, table_name):
        """Load data into database"""
        if not data:
            logger.warning(f"No data to load for {table_name}")
            return
        
        try:
            df = pd.DataFrame(data)
            df.to_sql(table_name, self.conn, if_exists="append", index=False)
            logger.info(f"Loaded {len(data)} records into {table_name}")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        logger.info("Calculating KPIs...")
        
        # Calculate OEE (simplified)
        query = """
        SELECT 
            equipment_id,
            COUNT(*) as total_readings,
            SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as normal_readings
        FROM equipment_readings
        WHERE timestamp >= datetime('now', '-24 hours')
        GROUP BY equipment_id
        """
        
        df = pd.read_sql_query(query, self.conn)
        
        if not df.empty:
            df["availability"] = df["normal_readings"] / df["total_readings"]
            df["performance"] = 0.85  # Placeholder
            df["quality"] = 0.95  # Placeholder
            df["oee"] = df["availability"] * df["performance"] * df["quality"]
            
            for _, row in df.iterrows():
                logger.info(f"Equipment {row['equipment_id']}: OEE = {row['oee']:.2%}")
        
        return df
    
    def run(self):
        """Execute ETL pipeline"""
        logger.info("Starting ETL Pipeline...")
        
        start_time = datetime.now()
        
        try:
            # EXTRACT
            equipment_raw, production_raw = self.extract_sample_data()
            
            # TRANSFORM
            equipment_transformed = self.transform_data(equipment_raw, "equipment")
            
            # LOAD
            self.load_data(equipment_transformed, "equipment_readings")
            self.load_data(production_raw, "production_data")
            
            # Calculate KPIs
            kpis = self.calculate_kpis()
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"ETL Pipeline completed in {duration:.2f} seconds")
            
            return {
                "status": "success",
                "records_processed": len(equipment_transformed) + len(production_raw),
                "duration": duration
            }
            
        except Exception as e:
            logger.error(f"ETL Pipeline failed: {e}")
            return {"status": "failed", "error": str(e)}
        
        finally:
            self.conn.close()

# Main execution
if __name__ == "__main__":
    pipeline = MiningETLPipeline()
    result = pipeline.run()
    print(f"\nResult: {result}")
