#!/usr/bin/env python3
"""
Clean all data - removes CSV files, checkpoints, and database table
Use this before starting a fresh scrape
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def clean_files():
    """Remove local CSV and checkpoint files"""
    files_to_remove = [
        'airr_product_data.csv',
        'airr_product_data_backup.csv',
        'scrape_checkpoint.json',
        'test_checkpoint.json'
    ]
    
    print("📁 Cleaning local files...")
    removed = 0
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"  ✓ Removed: {file}")
            removed += 1
    
    if removed == 0:
        print("  No local files to clean")
    else:
        print(f"  Total removed: {removed} files")

def clean_database():
    """Drop database table"""
    has_db_creds = all([
        os.getenv('SUPABASE_HOST'),
        os.getenv('SUPABASE_DBNAME'),
        os.getenv('SUPABASE_USER'),
        os.getenv('SUPABASE_PASSWORD'),
        os.getenv('SUPABASE_PORT')
    ])
    
    if not has_db_creds:
        print("\n🗄️  Database credentials not found - skipping database cleanup")
        return
    
    try:
        print("\n🗄️  Cleaning database...")
        
        DB_CONFIG = {
            'host': os.getenv('SUPABASE_HOST'),
            'dbname': os.getenv('SUPABASE_DBNAME'),
            'user': os.getenv('SUPABASE_USER'),
            'password': os.getenv('SUPABASE_PASSWORD'),
            'port': os.getenv('SUPABASE_PORT'),
            'sslmode': 'require'
        }
        
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"  ✓ Connected to {DB_CONFIG['host']}")
        
        with conn.cursor() as cur:
            # Get row count before deletion
            cur.execute("SELECT COUNT(*) FROM airr_product_availability")
            count = cur.fetchone()[0]
            
            # Drop table
            cur.execute("DROP TABLE IF EXISTS airr_product_availability CASCADE")
            conn.commit()
            
            print(f"  ✓ Dropped table 'airr_product_availability' ({count:,} rows deleted)")
        
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"  ✗ Database connection failed: {e}")
    except psycopg2.Error as e:
        if "does not exist" in str(e):
            print("  ✓ Table doesn't exist (nothing to clean)")
        else:
            print(f"  ✗ Database error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

def main():
    print("="*60)
    print("CLEAN ALL DATA - Fresh Start")
    print("="*60)
    print("\nThis will remove:")
    print("  - All CSV files (airr_product_data.csv)")
    print("  - All checkpoint files")
    print("  - Database table (airr_product_availability)")
    print()
    
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Cancelled - No data was deleted")
        return
    
    print("\n" + "="*60)
    
    clean_files()
    clean_database()
    
    print("\n" + "="*60)
    print("✅ CLEANUP COMPLETE")
    print("="*60)
    print("\nYou can now start a fresh scrape from product #1:")
    print("  python3 daily_scraper.py")
    print("="*60)

if __name__ == '__main__':
    main()
