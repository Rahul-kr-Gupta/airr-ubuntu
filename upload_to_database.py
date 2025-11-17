#!/usr/bin/env python3
import os
import csv
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('SUPABASE_HOST'),
    'dbname': os.getenv('SUPABASE_DBNAME'),
    'user': os.getenv('SUPABASE_USER'),
    'password': os.getenv('SUPABASE_PASSWORD'),
    'port': os.getenv('SUPABASE_PORT'),
    'sslmode': 'require'
}

CSV_FILE = 'airr_product_data.csv'
TABLE_NAME = 'airr_product_availability'

def create_table_if_not_exists(conn):
    """
    Create the table if it doesn't exist.
    Table schema:
    - id: Auto-incrementing primary key
    - product_code: Product code from CSV
    - product_name: Product name/description
    - location_name: Full warehouse location name
    - location_abbreviation: Short warehouse code
    - location_id: Location identifier
    - qty_available: Quantity available
    - qty_in_transit: Quantity in transit
    - qty_on_hand: Quantity on hand
    - qty_on_order: Quantity on order
    - scrape_status: Status of the scrape (success/error)
    - error_message: Error message if any
    - scraped_at: Timestamp when data was scraped
    - uploaded_at: Timestamp when data was uploaded to database
    """
    
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50) NOT NULL,
        product_name TEXT,
        location_name VARCHAR(100),
        location_abbreviation VARCHAR(20),
        location_id VARCHAR(20),
        qty_available INTEGER DEFAULT 0,
        qty_in_transit INTEGER DEFAULT 0,
        qty_on_hand INTEGER DEFAULT 0,
        qty_on_order INTEGER DEFAULT 0,
        scrape_status VARCHAR(20),
        error_message TEXT,
        scraped_at TIMESTAMP,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(product_code, location_id, scraped_at)
    );
    
    CREATE INDEX IF NOT EXISTS idx_product_code ON {TABLE_NAME}(product_code);
    CREATE INDEX IF NOT EXISTS idx_location_id ON {TABLE_NAME}(location_id);
    CREATE INDEX IF NOT EXISTS idx_scraped_at ON {TABLE_NAME}(scraped_at);
    """
    
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()
    
    print(f"✓ Table '{TABLE_NAME}' ready")

def read_csv_data(csv_file):
    """
    Read data from CSV file.
    Returns list of tuples ready for database insertion.
    """
    data = []
    scraped_at = datetime.now()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((
                row['product_code'],
                row['product_name'],
                row['location_name'],
                row['location_abbreviation'],
                row['location_id'],
                int(float(row['qty_available'])) if row['qty_available'] else 0,
                int(float(row['qty_in_transit'])) if row['qty_in_transit'] else 0,
                int(float(row['qty_on_hand'])) if row['qty_on_hand'] else 0,
                int(float(row['qty_on_order'])) if row['qty_on_order'] else 0,
                row['scrape_status'],
                row['error_message'] if row['error_message'] else None,
                scraped_at
            ))
    
    return data

def upload_data(conn, data):
    """
    Upload data to database using batch insert for performance.
    Uses ON CONFLICT to handle duplicates (update existing records).
    """
    
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (
        product_code, product_name, location_name, location_abbreviation,
        location_id, qty_available, qty_in_transit, qty_on_hand,
        qty_on_order, scrape_status, error_message, scraped_at
    ) VALUES %s
    ON CONFLICT (product_code, location_id, scraped_at) 
    DO UPDATE SET
        product_name = EXCLUDED.product_name,
        location_name = EXCLUDED.location_name,
        location_abbreviation = EXCLUDED.location_abbreviation,
        qty_available = EXCLUDED.qty_available,
        qty_in_transit = EXCLUDED.qty_in_transit,
        qty_on_hand = EXCLUDED.qty_on_hand,
        qty_on_order = EXCLUDED.qty_on_order,
        scrape_status = EXCLUDED.scrape_status,
        error_message = EXCLUDED.error_message,
        uploaded_at = CURRENT_TIMESTAMP
    """
    
    with conn.cursor() as cur:
        execute_values(cur, insert_query, data)
        conn.commit()
    
    print(f"✓ Uploaded {len(data)} rows to database")

def get_latest_stats(conn):
    """
    Get statistics about the latest upload.
    """
    
    stats_query = f"""
    SELECT 
        COUNT(DISTINCT product_code) as total_products,
        COUNT(DISTINCT location_id) as total_locations,
        COUNT(*) as total_rows,
        MAX(scraped_at) as latest_scrape,
        SUM(CASE WHEN scrape_status = 'success' THEN 1 ELSE 0 END) as successful_rows,
        SUM(CASE WHEN scrape_status = 'error' THEN 1 ELSE 0 END) as error_rows
    FROM {TABLE_NAME}
    WHERE scraped_at = (SELECT MAX(scraped_at) FROM {TABLE_NAME})
    """
    
    with conn.cursor() as cur:
        cur.execute(stats_query)
        result = cur.fetchone()
    
    return {
        'total_products': result[0],
        'total_locations': result[1],
        'total_rows': result[2],
        'latest_scrape': result[3],
        'successful_rows': result[4],
        'error_rows': result[5]
    }

def main():
    print("="*60)
    print("AIRR Product Data Upload to Supabase")
    print("="*60)
    
    if not os.path.exists(CSV_FILE):
        print(f"✗ Error: CSV file '{CSV_FILE}' not found")
        print("  Run the scraper first to generate the CSV file")
        return
    
    print(f"\n📁 CSV File: {CSV_FILE}")
    print(f"🗄️  Database: {DB_CONFIG['host']}")
    print(f"📊 Table: {TABLE_NAME}\n")
    
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Connected to database\n")
        
        print("Setting up database table...")
        create_table_if_not_exists(conn)
        print()
        
        print(f"Reading data from {CSV_FILE}...")
        data = read_csv_data(CSV_FILE)
        print(f"✓ Read {len(data)} rows from CSV\n")
        
        print("Uploading data to database...")
        upload_data(conn, data)
        print()
        
        print("Getting upload statistics...")
        stats = get_latest_stats(conn)
        print("\n" + "="*60)
        print("Upload Statistics")
        print("="*60)
        print(f"Products uploaded: {stats['total_products']}")
        print(f"Warehouse locations: {stats['total_locations']}")
        print(f"Total rows: {stats['total_rows']}")
        print(f"Successful: {stats['successful_rows']}")
        print(f"Errors: {stats['error_rows']}")
        print(f"Latest scrape: {stats['latest_scrape']}")
        print("="*60)
        
        conn.close()
        print("\n✅ Upload completed successfully!")
        
    except psycopg2.Error as e:
        print(f"\n✗ Database error: {e}")
        return
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return

if __name__ == '__main__':
    main()
