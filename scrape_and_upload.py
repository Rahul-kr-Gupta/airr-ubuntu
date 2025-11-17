#!/usr/bin/env python3
"""
Combined script that:
1. Scrapes product data from AIRR website
2. Uploads the data to Supabase PostgreSQL database

This is the main script to run daily for automated data collection.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_scraper():
    """Run the scraping script"""
    print("="*60)
    print("STEP 1: Scraping Product Data from AIRR Website")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    result = subprocess.run(['python3', 'daily_scraper.py'], capture_output=False)
    
    if result.returncode != 0:
        print("\n✗ Scraping failed!")
        return False
    
    print("\n✓ Scraping completed successfully!")
    return True

def run_upload():
    """Upload scraped data to database"""
    print("\n" + "="*60)
    print("STEP 2: Uploading Data to Supabase Database")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    result = subprocess.run(['python3', 'upload_to_database.py'], capture_output=False)
    
    if result.returncode != 0:
        print("\n✗ Database upload failed!")
        return False
    
    print("\n✓ Database upload completed successfully!")
    return True

def main():
    print("\n" + "="*60)
    print("AIRR Automated Data Collection & Upload Pipeline")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    # Step 1: Scrape data
    if not run_scraper():
        print("\n❌ Pipeline failed at scraping stage")
        sys.exit(1)
    
    # Step 2: Upload to database
    if not run_upload():
        print("\n❌ Pipeline failed at upload stage")
        sys.exit(1)
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")
    print("="*60)

if __name__ == '__main__':
    main()
