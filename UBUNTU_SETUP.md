# 🐧 Running AIRR Scraper on Ubuntu PC

Complete guide to set up and run the automated AIRR product scraper on your Ubuntu PC.

---

## 📋 Quick Start (5 Minutes)

### Step 1: Install Python and Dependencies

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version  # Should show 3.9 or higher
pip3 --version
```

### Step 2: Create Project Directory

```bash
# Create project folder
mkdir -p ~/airr-scraper
cd ~/airr-scraper
```

### Step 3: Download All Project Files

Copy all these files from Replit to `~/airr-scraper/`:

**Required Python Scripts:**
- `daily_scraper.py` - Main automation script
- `scrape_products_with_cookies.py` - Product scraper
- `login_and_save_cookies_.py` - Authentication handler
- `upload_to_database.py` - Database uploader
- `clean_all_data.py` - Manual cleanup tool

**Required Data Files:**
- `airr_sku_rows.csv` - Product codes list (2,968 products)
- `requirements.txt` - Python dependencies
- `.env.example` - Configuration template

### Step 4: Install Python Packages

```bash
pip3 install -r requirements.txt
```

**What gets installed:**
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML processor
- `pandas` - Data manipulation
- `playwright` - Browser automation
- `python-dotenv` - Environment variables
- `psycopg2-binary` - PostgreSQL database

### Step 5: Install Playwright Browser

```bash
# Install Chromium browser for Playwright
python3 -m playwright install chromium

# Install system dependencies
python3 -m playwright install-deps chromium
```

**If you get permission errors:**
```bash
sudo python3 -m playwright install-deps chromium
```

### Step 6: Configure Your Credentials

```bash
# Copy example configuration
cp .env.example .env

# Edit with your credentials
nano .env
```

**Fill in your actual credentials:**

```bash
# AIRR Website Login
airr_USERNAME=your_actual_username
airr_PASSWORD=your_actual_password

# Supabase Database (get from Supabase dashboard)
SUPABASE_HOST=aws-1-ap-south-1.pooler.supabase.com
SUPABASE_DBNAME=postgres
SUPABASE_USER=postgres.yourprojectid
SUPABASE_PASSWORD=your_database_password
SUPABASE_PORT=6543
```

**Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

### Step 7: Test Authentication

```bash
python3 login_and_save_cookies_.py
```

**Expected output:**
```
Starting login process for user: your_username
✓ Playwright browsers ready
Navigating to login page...
✓ localStorage populated with token
✓ Success! Saved authentication data to cookies.json
```

### Step 8: Run the Full Scraper

```bash
python3 daily_scraper.py
```

This will:
1. ✅ Clean old data (CSV, checkpoints, database)
2. ✅ Authenticate to AIRR website
3. ✅ Scrape all 2,968 products
4. ✅ Upload to Supabase database
5. ✅ Show completion summary

---

## 🔄 What Happens When You Run

### Automatic Cleanup (Fresh Start)

Every time you run `daily_scraper.py`, it automatically:

```
🧹 CLEANUP PHASE:
  - Deletes airr_product_data.csv
  - Deletes scrape_checkpoint.json
  - Drops database table (airr_product_availability)
  
🔐 AUTHENTICATION PHASE:
  - Gets fresh cookies and token
  - Saves to cookies.json
  
🕷️ SCRAPING PHASE:
  - Starts from product #1
  - Scrapes all 2,968 products
  - Saves to CSV file
  - Auto-refreshes authentication every 10 products
  
📤 UPLOAD PHASE:
  - Creates fresh database table
  - Uploads ~30,000 rows (11 warehouses × 2,968 products)
  - Creates indexes for fast queries
```

### Daily Data Behavior

Each run **replaces** the previous data with fresh data:

```
Day 1: Scrape → Database has Day 1 inventory
Day 2: Clean → Scrape → Database has Day 2 inventory (Day 1 deleted)
Day 3: Clean → Scrape → Database has Day 3 inventory (Day 2 deleted)
```

You always have the **latest inventory snapshot**.

---

## ⏰ Set Up Daily Automation (Cron)

### Run automatically every day at 5 PM AEST

1. **Edit crontab:**
```bash
crontab -e
```

2. **Add this line:**
```bash
0 17 * * * cd ~/airr-scraper && /usr/bin/python3 daily_scraper.py >> ~/airr-scraper/scraper.log 2>&1
```

3. **Save and exit**

This will:
- Run daily at 5:00 PM
- Automatically clean old data
- Scrape fresh products
- Upload to database
- Save logs to `scraper.log`

### Check Logs

```bash
# View live logs
tail -f ~/airr-scraper/scraper.log

# View last 50 lines
tail -n 50 ~/airr-scraper/scraper.log

# Search for errors
grep ERROR ~/airr-scraper/scraper.log
```

### Check Cron Status

```bash
# List all cron jobs
crontab -l

# Check if cron is running
systemctl status cron
```

---

## 📁 Output Files

After running, you'll have:

```
~/airr-scraper/
├── airr_product_data.csv         # Fresh scraped data (~30,000 rows)
├── cookies.json                   # Authentication data
├── scraper.log                    # Execution logs (if using cron)
└── scrape_checkpoint.json         # (Auto-deleted after completion)
```

### CSV File Structure

```csv
product_code,product_name,location_name,location_abbreviation,location_id,
qty_available,qty_in_transit,qty_on_hand,qty_on_order,scrape_status,
error_message,scraped_at
```

Example row:
```
112049,Cable Ties 200mm x 4.8mm White (Pk100),Adelaide,ADL,3,
500,0,500,0,success,,2025-11-17 17:05:23
```

---

## 🗄️ Database Access

### View Your Data in Supabase

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to "Table Editor"
4. View `airr_product_availability` table

### Query Examples

**Get product availability across all locations:**
```sql
SELECT 
    product_code,
    product_name,
    location_abbreviation,
    qty_available,
    qty_on_hand
FROM airr_product_availability
WHERE product_code = '112049'
ORDER BY location_abbreviation;
```

**Find products with low stock:**
```sql
SELECT DISTINCT 
    product_code,
    product_name,
    SUM(qty_available) as total_available
FROM airr_product_availability
GROUP BY product_code, product_name
HAVING SUM(qty_available) < 10
ORDER BY total_available;
```

**Get latest scrape timestamp:**
```sql
SELECT MAX(scraped_at) as last_scrape_time
FROM airr_product_availability;
```

---

## 🛠️ Manual Operations

### Clean All Data (Manual)

If you want to clean without running the scraper:

```bash
python3 clean_all_data.py
```

This interactive script will:
- Ask for confirmation
- Delete CSV files
- Delete checkpoints
- Drop database table

### Run in Background

```bash
# Start in background
nohup python3 daily_scraper.py > scraper.log 2>&1 &

# Check if running
ps aux | grep daily_scraper

# Stop background process
pkill -f daily_scraper
```

### Resume from Checkpoint (Crash Recovery)

If the scraper crashes mid-run, resume without cleanup:

```bash
# Don't run daily_scraper.py (it will clean everything)
# Instead run the scraper directly:
python3 scrape_products_with_cookies.py

# Then upload:
python3 upload_to_database.py
```

---

## 🧪 Testing

### Test with Small Dataset

Edit `airr_sku_rows.csv` to include only 5-10 products for testing:

```bash
# Backup original file
cp airr_sku_rows.csv airr_sku_rows_full.csv

# Create test file with first 10 products
head -n 11 airr_sku_rows_full.csv > airr_sku_rows.csv

# Run scraper
python3 daily_scraper.py

# Restore full product list when ready
mv airr_sku_rows_full.csv airr_sku_rows.csv
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'playwright'"

```bash
pip3 install -r requirements.txt
```

### "playwright._impl._api_types.Error: Executable doesn't exist"

```bash
python3 -m playwright install chromium
python3 -m playwright install-deps chromium
```

### "No token found in authentication data"

```bash
# Re-run login script
python3 login_and_save_cookies_.py

# Check cookies.json was created
cat cookies.json | grep token
```

### "Database connection failed"

Check your `.env` file:
```bash
cat .env
```

Make sure database credentials are correct.

### Permission Errors

```bash
# Make scripts executable
chmod +x *.py

# If Playwright needs system deps:
sudo python3 -m playwright install-deps chromium
```

### Scraper Stuck or Frozen

```bash
# Kill the process
pkill -f daily_scraper

# Check for zombie processes
ps aux | grep daily_scraper

# Clean and restart
python3 clean_all_data.py
python3 daily_scraper.py
```

---

## 📊 Performance

### Expected Runtime

- **Duration:** 2-3 hours for all 2,968 products
- **Speed:** ~15-20 products per minute
- **CPU:** Low (mostly network waiting)
- **RAM:** ~500MB
- **Disk:** ~10MB for CSV output

### Resource Usage

```bash
# Monitor while running
top -p $(pgrep -f daily_scraper)

# Check disk space
df -h ~

# Check memory
free -h
```

---

## 💻 System Requirements

### Minimum Requirements

- **OS:** Ubuntu 20.04 or higher (also works on Debian, Linux Mint)
- **Python:** 3.9 or higher
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 100MB free space
- **Internet:** Stable connection (required for scraping)

### Tested On

- ✅ Ubuntu 22.04 LTS
- ✅ Ubuntu 20.04 LTS
- ✅ Debian 11
- ✅ Linux Mint 21

---

## 🔐 Security Best Practices

1. **Protect your credentials:**
   ```bash
   chmod 600 .env  # Only you can read
   ```

2. **Never commit `.env` to git:**
   ```bash
   echo ".env" >> .gitignore
   ```

3. **Keep backups secure:**
   ```bash
   # Encrypt backups if storing
   tar -czf backup.tar.gz *.csv
   gpg -c backup.tar.gz
   ```

4. **Rotate passwords regularly**

---

## 📞 Support

### Check Logs First

```bash
# Last 100 lines of scraper output
tail -n 100 ~/airr-scraper/scraper.log

# Search for errors
grep -i error ~/airr-scraper/scraper.log

# Search for specific product
grep "112049" ~/airr-scraper/scraper.log
```

### Common Solutions

| Problem | Solution |
|---------|----------|
| Login fails | Check `airr_USERNAME` and `airr_PASSWORD` in `.env` |
| No data in database | Check `SUPABASE_*` credentials in `.env` |
| Scraper stops | Check logs, might need to resume from checkpoint |
| Cron not running | Check `systemctl status cron` |

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Full workflow (recommended)
python3 daily_scraper.py

# Just login test
python3 login_and_save_cookies_.py

# Manual cleanup
python3 clean_all_data.py

# View logs
tail -f scraper.log

# Edit cron schedule
crontab -e

# Stop scraper
pkill -f daily_scraper
```

---

**You're all set! Your Ubuntu PC is now ready to scrape AIRR products daily.** 🎉
