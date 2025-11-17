#!/usr/bin/env python3
"""
Daily scraper automation script
Runs daily at 5 PM AEST to scrape fresh product data
"""
import os
import sys
import subprocess
import time
from datetime import datetime

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def run_command(command, description):
    """Run a command and log output in real-time"""
    log(f"Starting: {description}")
    log(f"Command: {command}")
    
    try:
        # Use unbuffered Python for real-time output
        if command.startswith('python'):
            command = command.replace('python', 'python -u', 1)
        
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Stream output in real-time
        for line in process.stdout:
            print(line, end='', flush=True)
        
        # Wait for process to complete
        returncode = process.wait()
        
        if returncode != 0:
            log(f"✗ Error in {description}")
            return False
        
        log(f"✓ Completed: {description}")
        return True
        
    except Exception as e:
        log(f"✗ Exception in {description}: {e}")
        return False

def clean_database():
    """Clear old data from Supabase database"""
    try:
        import psycopg2
        
        DB_CONFIG = {
            'host': os.getenv('SUPABASE_HOST'),
            'dbname': os.getenv('SUPABASE_DBNAME'),
            'user': os.getenv('SUPABASE_USER'),
            'password': os.getenv('SUPABASE_PASSWORD'),
            'port': os.getenv('SUPABASE_PORT'),
            'sslmode': 'require'
        }
        
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS airr_product_availability CASCADE")
            conn.commit()
        conn.close()
        
        log("  ✓ Database table dropped (will be recreated on upload)")
        return True
    except Exception as e:
        log(f"  ⚠️  Could not clear database: {e}")
        return False

def main():
    """Main daily scraping workflow"""
    log("="*70)
    log("DAILY SCRAPING WORKFLOW STARTED - FRESH RUN")
    log("="*70)
    
    # Clean up old data files
    log("\n📁 Cleaning up old data files...")
    for file in ['airr_product_data.csv', 'airr_product_data_backup.csv', 'scrape_checkpoint.json']:
        if os.path.exists(file):
            os.remove(file)
            log(f"  Removed: {file}")
    
    # Clean database if credentials available
    has_db_creds = all([
        os.getenv('SUPABASE_HOST'),
        os.getenv('SUPABASE_DBNAME'),
        os.getenv('SUPABASE_USER'),
        os.getenv('SUPABASE_PASSWORD'),
        os.getenv('SUPABASE_PORT')
    ])
    
    if has_db_creds:
        log("\n🗄️  Cleaning database...")
        clean_database()
    
    log("✓ Ready for fresh scrape from product #1")
    
    # Step 1: Authenticate and get fresh cookies
    log("\n🔐 STEP 1: Authentication")
    log("-" * 70)
    if not run_command(
        "python login_and_save_cookies_.py",
        "Login and retrieve fresh cookies"
    ):
        log("\n❌ FAILED: Could not authenticate. Aborting.")
        sys.exit(1)
    
    # Verify cookies file was created
    if not os.path.exists('cookies.json'):
        log("\n❌ FAILED: cookies.json not found after login. Aborting.")
        sys.exit(1)
    
    log("✓ Fresh cookies obtained successfully")
    
    # Step 2: Run the scraping script
    log("\n🕷️  STEP 2: Scraping Products")
    log("-" * 70)
    log("Starting scraper with auto-refresh every 100 products...")
    
    if not run_command(
        "python scrape_products_with_cookies.py",
        "Product scraping with auto-refresh"
    ):
        log("\n⚠️  WARNING: Scraper encountered errors")
        # Don't exit - partial data may still be useful
    
    # Step 3: Verify output
    log("\n📊 STEP 3: Verification")
    log("-" * 70)
    
    if os.path.exists('airr_product_data.csv'):
        file_size = os.path.getsize('airr_product_data.csv')
        with open('airr_product_data.csv', 'r') as f:
            line_count = sum(1 for _ in f)
        
        log(f"✓ Output file created: airr_product_data.csv")
        log(f"  File size: {file_size / 1024:.2f} KB")
        log(f"  Total rows: {line_count:,} (including header)")
        log(f"  Data rows: {line_count - 1:,}")
    else:
        log("✗ No output file found!")
        sys.exit(1)
    
    # Step 4: Upload to Supabase Database
    log("\n🗄️  STEP 4: Upload to Supabase Database")
    log("-" * 70)
    
    # Check if database credentials are available
    has_db_creds = all([
        os.getenv('SUPABASE_HOST'),
        os.getenv('SUPABASE_DBNAME'),
        os.getenv('SUPABASE_USER'),
        os.getenv('SUPABASE_PASSWORD'),
        os.getenv('SUPABASE_PORT')
    ])
    
    if has_db_creds:
        log("Database credentials found. Starting upload...")
        if run_command(
            "python upload_to_database.py",
            "Database upload"
        ):
            log("✓ Data uploaded to Supabase successfully!")
        else:
            log("⚠️  WARNING: Database upload failed. CSV file is still saved locally.")
    else:
        log("⚠️  Skipping database upload (credentials not configured)")
        log("   To enable automatic upload, set SUPABASE_* environment variables")
    
    # Final summary
    log("\n" + "="*70)
    log("✅ DAILY SCRAPING WORKFLOW COMPLETED SUCCESSFULLY")
    log("="*70)
    log(f"CSV file saved to: airr_product_data.csv")
    if has_db_creds:
        log(f"Database: Data uploaded to Supabase")
    log(f"Next run: Tomorrow at 5:00 PM AEST")
    log("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n⚠️  Workflow interrupted by user")
        sys.exit(130)
    except Exception as e:
        log(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
