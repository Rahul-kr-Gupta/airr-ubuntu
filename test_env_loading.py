#!/usr/bin/env python3
"""
Test if .env file is being loaded correctly
Run this on Ubuntu to verify credentials are working
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from script directory
env_path = Path(__file__).parent / '.env'
print(f"🔍 Testing .env file loading...")
print(f"   Script directory: {Path(__file__).parent.absolute()}")
print(f"   Expected .env location: {env_path.absolute()}")
print(f"   .env file exists: {env_path.exists()}")
print()

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Check each credential
credentials = {
    'airr_USERNAME': os.getenv('airr_USERNAME'),
    'airr_PASSWORD': os.getenv('airr_PASSWORD'),
    'SUPABASE_HOST': os.getenv('SUPABASE_HOST'),
    'SUPABASE_DBNAME': os.getenv('SUPABASE_DBNAME'),
    'SUPABASE_USER': os.getenv('SUPABASE_USER'),
    'SUPABASE_PASSWORD': os.getenv('SUPABASE_PASSWORD'),
    'SUPABASE_PORT': os.getenv('SUPABASE_PORT')
}

print("📋 Checking credentials:")
print("="*60)

all_found = True
for key, value in credentials.items():
    if value:
        # Show first few characters for verification
        if 'PASSWORD' in key or 'TOKEN' in key:
            display_value = value[:4] + '***' if len(value) > 4 else '***'
        else:
            display_value = value[:20] + '...' if len(value) > 20 else value
        print(f"✓ {key:20s} = {display_value}")
    else:
        print(f"✗ {key:20s} = NOT FOUND")
        all_found = False

print("="*60)

if all_found:
    print("\n✅ SUCCESS! All credentials loaded correctly from .env file")
    print("   You can now run the scraper on Ubuntu")
else:
    print("\n❌ ERROR! Some credentials are missing")
    print("\n📝 Troubleshooting steps:")
    print("   1. Check that .env file exists in the same directory as scripts")
    print("   2. Open .env file and verify all credentials are set")
    print("   3. Make sure there are no extra spaces or quotes around values")
    print("   4. Make sure each line follows format: KEY=value")
    print("\n   Example .env file format:")
    print("   airr_USERNAME=your_username")
    print("   airr_PASSWORD=your_password")
    print("   SUPABASE_HOST=aws-0-ap-southeast-2.pooler.supabase.com")
