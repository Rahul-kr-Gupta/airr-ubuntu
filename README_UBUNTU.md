# 🐧 AIRR Scraper for Ubuntu PC

Automated daily web scraper for AIRR product inventory (2,968 products × 11 warehouses).

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Download files to ~/airr-scraper
cd ~/airr-scraper

# 2. Run automated setup
./ubuntu_setup.sh

# 3. Configure credentials
nano .env

# 4. Test setup
python3 test_setup.py

# 5. Run scraper
python3 daily_scraper.py
```

**Done!** Your data will be in `airr_product_data.csv` and uploaded to Supabase.

---

## 📋 What This Does

Every time you run the scraper:

1. **Cleans** old data (CSV, checkpoints, database)
2. **Authenticates** to AIRR website
3. **Scrapes** all 2,968 products from 11 warehouse locations
4. **Saves** to CSV (~30,000 rows)
5. **Uploads** to Supabase PostgreSQL database

**Runtime:** 2-3 hours  
**Output:** Fresh inventory snapshot

---

## 📁 Files You Need

### Download from Replit

**Essential:**
- `daily_scraper.py` - Main automation
- `scrape_products_with_cookies.py` - Scraper engine
- `login_and_save_cookies_.py` - Authentication
- `upload_to_database.py` - Database uploader
- `airr_sku_rows.csv` - **2,968 product codes (REQUIRED!)**
- `requirements.txt` - Python dependencies
- `.env.example` - Configuration template

**Helpers:**
- `ubuntu_setup.sh` - Automated setup script
- `test_setup.py` - Verify installation
- `clean_all_data.py` - Manual cleanup tool

**Documentation:**
- `UBUNTU_SETUP.md` - Detailed setup guide
- `DOWNLOAD_GUIDE.md` - How to get files from Replit
- `CLEAN_AND_RESTART.md` - Data cleanup guide

---

## 🚀 Setup Methods

### Method 1: Automated (Recommended)

```bash
cd ~/airr-scraper
./ubuntu_setup.sh
```

This will:
- Install Python packages
- Install Playwright browser
- Create `.env` file
- Make scripts executable

Then edit your credentials:
```bash
nano .env
```

### Method 2: Manual

```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip -y

# Install packages
pip3 install -r requirements.txt

# Install Playwright
python3 -m playwright install chromium
sudo python3 -m playwright install-deps chromium

# Configure
cp .env.example .env
nano .env
```

---

## ⚙️ Configuration (.env file)

```bash
# AIRR Login
airr_USERNAME=your_actual_username
airr_PASSWORD=your_actual_password

# Supabase Database
SUPABASE_HOST=aws-1-ap-south-1.pooler.supabase.com
SUPABASE_DBNAME=postgres
SUPABASE_USER=postgres.yourprojectid
SUPABASE_PASSWORD=your_database_password
SUPABASE_PORT=6543
```

Get Supabase credentials from:
1. https://supabase.com/dashboard
2. Your project → Settings → Database
3. Copy connection details

---

## 🎯 Running the Scraper

### One-Time Run

```bash
python3 daily_scraper.py
```

This runs the complete workflow with automatic cleanup.

### Daily Automation (Cron)

Run automatically every day at 5 PM:

```bash
crontab -e
```

Add this line:
```
0 17 * * * cd ~/airr-scraper && python3 daily_scraper.py >> scraper.log 2>&1
```

Check logs:
```bash
tail -f ~/airr-scraper/scraper.log
```

---

## 📊 Output

### CSV File

`airr_product_data.csv` contains:
- Product code & name
- 11 warehouse locations per product
- Quantities: Available, In Transit, On Hand, On Order
- Timestamps

**Size:** ~30,000 rows (2,968 products × 11 locations)

### Database

Table: `airr_product_availability` in Supabase

**Query example:**
```sql
SELECT product_code, location_abbreviation, qty_available
FROM airr_product_availability
WHERE product_code = '112049';
```

---

## 🔄 How Cleanup Works

**Every run automatically:**

```
🧹 CLEANUP:
  - Deletes airr_product_data.csv
  - Deletes scrape_checkpoint.json
  - Drops database table
  
🔐 LOGIN:
  - Gets fresh authentication
  
🕷️ SCRAPE:
  - Starts from product #1
  - Scrapes all 2,968 products
  
📤 UPLOAD:
  - Creates fresh database table
  - Uploads all data
```

**Result:** Each run gives you the latest inventory snapshot (old data is replaced).

---

## 🧪 Testing

### Test Installation

```bash
python3 test_setup.py
```

Checks:
- ✅ Python version
- ✅ Required packages
- ✅ Configuration file
- ✅ Required scripts
- ✅ Playwright browser

### Test Authentication

```bash
python3 login_and_save_cookies_.py
```

Should output:
```
✓ localStorage populated with token
✓ Success! Saved authentication data
```

### Test with Small Dataset

```bash
# Create test file with 5 products
head -n 6 airr_sku_rows.csv > test_products.csv
mv test_products.csv airr_sku_rows.csv

# Run scraper (will only scrape 5 products)
python3 daily_scraper.py
```

---

## 🛠️ Troubleshooting

### Check Setup Status

```bash
python3 test_setup.py
```

### Common Issues

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | `pip3 install -r requirements.txt` |
| "Playwright browser missing" | `python3 -m playwright install chromium` |
| "No token found" | Check airr_USERNAME and airr_PASSWORD in .env |
| "Database connection failed" | Check SUPABASE_* credentials in .env |
| "Permission denied" | `chmod +x *.py *.sh` |

### View Logs

```bash
# Last 50 lines
tail -n 50 scraper.log

# Live monitoring
tail -f scraper.log

# Search for errors
grep ERROR scraper.log
```

### Manual Cleanup

```bash
python3 clean_all_data.py
```

---

## 📖 Documentation

- **UBUNTU_SETUP.md** - Complete setup instructions
- **DOWNLOAD_GUIDE.md** - How to get files from Replit
- **CLEAN_AND_RESTART.md** - Data cleanup details
- **DATABASE_SETUP.md** - Database configuration

---

## 💻 System Requirements

- Ubuntu 20.04+ (also works on Debian, Linux Mint)
- Python 3.9+
- 2GB RAM (4GB recommended)
- 100MB disk space
- Stable internet connection

---

## 🔐 Security

```bash
# Protect credentials
chmod 600 .env

# Never commit to git
echo ".env" >> .gitignore
```

---

## 📞 Quick Commands

```bash
# Run scraper
python3 daily_scraper.py

# Test setup
python3 test_setup.py

# Test login only
python3 login_and_save_cookies_.py

# Manual cleanup
python3 clean_all_data.py

# View logs
tail -f scraper.log

# Stop scraper
pkill -f daily_scraper
```

---

## 📈 Performance

- **Duration:** 2-3 hours for 2,968 products
- **Speed:** ~15-20 products/minute
- **CPU:** Low (network-bound)
- **RAM:** ~500MB
- **Disk:** ~10MB output

---

**Ready to start? Run `./ubuntu_setup.sh` and follow the prompts!** 🚀
