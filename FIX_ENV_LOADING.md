# ✅ FIXED: .env File Loading Issue on Ubuntu

## What Was The Problem?

The scripts were using `load_dotenv()` without specifying the path to the `.env` file. This caused the scripts to only work if you ran them from the exact directory where the `.env` file was located.

**Example of the problem:**
```bash
cd ~/airr-scraper
python3 scrape_products_with_cookies.py  # ✅ Works

cd ~/Desktop
python3 ~/airr-scraper/scrape_products_with_cookies.py  # ❌ Doesn't work!
```

## What Was Fixed?

All Python scripts now use an absolute path to load the `.env` file, regardless of where you run the script from:

**Before (problematic code):**
```python
from dotenv import load_dotenv
load_dotenv()  # Only works if .env is in current directory
```

**After (fixed code):**
```python
from pathlib import Path
from dotenv import load_dotenv

# Load .env from script directory, not current directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
```

## Files Updated

✅ All scripts now load `.env` correctly:
- `scrape_products_with_cookies.py`
- `login_and_save_cookies_.py`
- `upload_to_database.py`
- `clean_all_data.py`
- `test_setup.py`

## New Diagnostic Tool

**New file:** `test_env_loading.py`

This script helps you verify that `.env` file is being loaded correctly:

```bash
python3 test_env_loading.py
```

**Example output:**
```
🔍 Testing .env file loading...
   Script directory: /home/user/airr-scraper
   Expected .env location: /home/user/airr-scraper/.env
   .env file exists: True

📋 Checking credentials:
============================================================
✓ airr_USERNAME        = WEBBARRY
✓ airr_PASSWORD        = Petf***
✓ SUPABASE_HOST        = aws-1-ap-south-1.poo...
✓ SUPABASE_DBNAME      = postgres
✓ SUPABASE_USER        = postgres.odpysbkgdzw...
✓ SUPABASE_PASSWORD    = IqxE***
✓ SUPABASE_PORT        = 6543
============================================================

✅ SUCCESS! All credentials loaded correctly from .env file
   You can now run the scraper on Ubuntu
```

## How To Use On Ubuntu

### 1. Download Updated Files

Download these updated files from Replit to your Ubuntu PC:
- `scrape_products_with_cookies.py`
- `login_and_save_cookies_.py`
- `upload_to_database.py`
- `clean_all_data.py`
- `test_setup.py`
- `test_env_loading.py` (NEW!)
- `UBUNTU_TROUBLESHOOTING.md` (NEW!)

**OR** just download the entire project as ZIP from Replit:
- Click ☰ menu → "Download as zip"
- Extract on Ubuntu and replace old files

### 2. Test .env Loading

```bash
cd ~/airr-scraper
python3 test_env_loading.py
```

You should see all credentials loaded with ✓ checkmarks.

### 3. Run Full System Test

```bash
python3 test_setup.py
```

Should show: ✅ ALL TESTS PASSED!

### 4. Run The Scraper

```bash
python3 daily_scraper.py
```

## What If It Still Doesn't Work?

### Check .env File Format

Open your `.env` file:
```bash
cat .env
```

Make sure it looks like this (no extra spaces, no quotes):
```
airr_USERNAME=WEBBARRY
airr_PASSWORD=your_password
SUPABASE_HOST=aws-0-ap-southeast-2.pooler.supabase.com
SUPABASE_DBNAME=postgres
SUPABASE_USER=postgres.yourprojectid
SUPABASE_PASSWORD=your_db_password
SUPABASE_PORT=6543
```

### Common Mistakes

❌ **WRONG:**
```
airr_USERNAME = WEBBARRY          # Extra spaces
airr_PASSWORD="password"          # Quotes
SUPABASE_HOST=your_host           # Placeholder value
```

✅ **CORRECT:**
```
airr_USERNAME=WEBBARRY
airr_PASSWORD=actual_password
SUPABASE_HOST=aws-0-ap-southeast-2.pooler.supabase.com
```

### Still Having Issues?

See the new `UBUNTU_TROUBLESHOOTING.md` file for detailed troubleshooting steps.

## Bonus: Real-Time Database Updates Now Working!

The scraper now pushes data to Supabase **in real-time** as it scrapes each product:

```
[1/2968] Scraping: 10002
  ✓ Silo Bag Grain Bag 9ft x 75mt rf ** - 11 locations
    💾 Pushed 11 rows to database  ← NEW!
```

Benefits:
- ✅ See data appearing live in Supabase dashboard
- ✅ No need to wait 2-3 hours to see results
- ✅ Data is safe even if scraper crashes mid-way
- ✅ Can query database while scraping is still running

---

## Summary

✅ All `.env` loading issues fixed
✅ New diagnostic tool to verify credentials
✅ New troubleshooting guide for Ubuntu
✅ Real-time database uploads working
✅ Ready to run on Ubuntu PC!

**Next Steps:**
1. Download updated files to Ubuntu
2. Run `python3 test_env_loading.py`
3. Run `python3 daily_scraper.py`
4. Watch live updates in Supabase dashboard!
