# 🔧 Ubuntu Troubleshooting Guide

## Problem: .env File Not Loading

### Symptoms
- Scripts show: "⚠️ WARNING: .env file not found or empty!"
- Credentials show as "NOT FOUND" 
- Database connection fails

### Solution

**Step 1: Verify .env file exists**
```bash
cd ~/airr-scraper
ls -la .env
```

You should see: `.env` file listed

**Step 2: Check file permissions**
```bash
chmod 644 .env
```

**Step 3: View .env content**
```bash
cat .env
```

Make sure it contains all credentials (no placeholders like "your_username"):
```
airr_USERNAME=WEBBARRY
airr_PASSWORD=actual_password_here
SUPABASE_HOST=aws-0-ap-southeast-2.pooler.supabase.com
SUPABASE_DBNAME=postgres
SUPABASE_USER=postgres.odpysbkgdzwdtumfjcwe
SUPABASE_PASSWORD=actual_db_password_here
SUPABASE_PORT=6543
```

**Step 4: Test .env loading**
```bash
python3 test_env_loading.py
```

This will show exactly which credentials are loaded and which are missing.

**Step 5: Common .env file mistakes**

❌ **WRONG:**
```
airr_USERNAME = WEBBARRY          # Extra spaces around =
airr_PASSWORD="password"          # Quotes not needed
SUPABASE_HOST = your_host         # Placeholder value
```

✅ **CORRECT:**
```
airr_USERNAME=WEBBARRY
airr_PASSWORD=actual_password
SUPABASE_HOST=aws-0-ap-southeast-2.pooler.supabase.com
```

**Step 6: Recreate .env file if needed**
```bash
cp .env.example .env
nano .env
# Fill in your actual credentials
# Save: Ctrl+X, Y, Enter
```

---

## Problem: Playwright Browser Not Found

### Symptoms
- Error: "Executable doesn't exist"
- Error: "Browser not installed"

### Solution
```bash
python3 -m playwright install chromium
```

---

## Problem: Import Errors (ModuleNotFoundError)

### Symptoms
- Error: "No module named 'playwright'"
- Error: "No module named 'psycopg2'"

### Solution
```bash
pip3 install -r requirements.txt
```

Or install packages individually:
```bash
pip3 install playwright beautifulsoup4 lxml pandas python-dotenv psycopg2-binary
```

---

## Problem: Database Connection Fails

### Symptoms
- Error: "could not connect to server"
- Error: "password authentication failed"
- TimeoutError connecting to database

### Solution

**Step 1: Verify credentials in .env**
```bash
python3 test_env_loading.py
```

**Step 2: Test database connection**
```bash
python3 -c "
import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

try:
    conn = psycopg2.connect(
        host=os.getenv('SUPABASE_HOST'),
        dbname=os.getenv('SUPABASE_DBNAME'),
        user=os.getenv('SUPABASE_USER'),
        password=os.getenv('SUPABASE_PASSWORD'),
        port=os.getenv('SUPABASE_PORT'),
        sslmode='require'
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
```

**Step 3: Check Supabase credentials**
- Go to Supabase Dashboard → Project Settings → Database
- Copy exact values (no extra spaces)
- Connection Pooler should use Transaction mode, port 6543
- Make sure "Use connection pooling" is enabled

---

## Problem: Scraper Runs But No Data

### Symptoms
- Scraper completes but CSV file is empty
- Database has 0 rows after scraping

### Solution

**Step 1: Check authentication**
```bash
python3 login_and_save_cookies_.py
```

Should create `cookies.json` file successfully.

**Step 2: Verify airr_sku_rows.csv exists**
```bash
ls -lh airr_sku_rows.csv
```

Should show ~2,968 products.

**Step 3: Check scraper logs**
Run scraper and look for errors:
```bash
python3 daily_scraper.py 2>&1 | tee scraper.log
```

---

## Problem: Permission Denied Errors

### Symptoms
- Error: "Permission denied" when running scripts
- Error: "cannot execute binary file"

### Solution
```bash
chmod +x ubuntu_setup.sh
chmod +x test_env_loading.py
chmod +x daily_scraper.py
```

---

## Getting Help

**Diagnostic Information**

Run these commands and save the output:

```bash
# System info
python3 --version
pip3 --version
which python3

# .env file test
python3 test_env_loading.py

# Full system test
python3 test_setup.py

# Package versions
pip3 list | grep -E "(playwright|psycopg2|pandas|beautifulsoup4|dotenv)"
```

**Quick Reset**

If everything is broken, start fresh:

```bash
# Backup your .env file
cp .env .env.backup

# Clean everything
rm -f cookies.json scrape_checkpoint.json airr_product_data.csv

# Re-run setup
./ubuntu_setup.sh

# Restore your credentials
cp .env.backup .env

# Test again
python3 test_env_loading.py
python3 test_setup.py
```
