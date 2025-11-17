# 📥 Download Guide - Moving Files from Replit to Ubuntu PC

This guide shows you how to download all the scraper files from Replit to your Ubuntu PC.

---

## Method 1: Download as ZIP (Easiest)

### Step 1: Download from Replit

1. In your Replit project, click the **☰** menu (top left)
2. Click **Download as zip**
3. Save `airr-scraper.zip` to your Downloads folder

### Step 2: Extract on Ubuntu

```bash
# Navigate to Downloads
cd ~/Downloads

# Extract the zip file
unzip airr-scraper.zip -d ~/airr-scraper

# Navigate to project folder
cd ~/airr-scraper

# List files to verify
ls -la
```

You should see all the Python scripts, CSV files, and configuration files.

---

## Method 2: Download Individual Files

### From Replit Web Interface

1. Click on each file in the Replit file tree
2. Click the **⋮** menu (three dots)
3. Select **Download**
4. Save to `~/airr-scraper/` on your Ubuntu PC

### Required Files to Download

**Core Scripts (Required):**
- `daily_scraper.py`
- `scrape_products_with_cookies.py`
- `login_and_save_cookies_.py`
- `upload_to_database.py`
- `clean_all_data.py`

**Data Files (Required):**
- `airr_sku_rows.csv` (Product codes - very important!)
- `requirements.txt`
- `.env.example`

**Setup Helpers (Recommended):**
- `ubuntu_setup.sh`
- `test_setup.py`
- `UBUNTU_SETUP.md`
- `DOWNLOAD_GUIDE.md`
- `CLEAN_AND_RESTART.md`

**Optional Documentation:**
- `DATABASE_SETUP.md`
- `README.md`

---

## Method 3: Using Git (Advanced)

### If you have git configured on Replit:

```bash
# On your Ubuntu PC
cd ~
git clone https://github.com/yourusername/airr-scraper.git
cd airr-scraper
```

---

## Method 4: Using SCP from Ubuntu (Advanced)

If you have SSH access to a server where files are stored:

```bash
scp -r user@server:/path/to/airr-scraper ~/airr-scraper
```

---

## Verify Downloaded Files

After downloading, verify all files are present:

```bash
cd ~/airr-scraper
python3 test_setup.py
```

This will check:
- ✅ All required Python scripts
- ✅ Data files (airr_sku_rows.csv)
- ✅ Configuration templates

---

## Next Steps

After downloading files to `~/airr-scraper/`:

1. **Run the automated setup:**
   ```bash
   cd ~/airr-scraper
   ./ubuntu_setup.sh
   ```

2. **Or follow manual setup:**
   ```bash
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Install Playwright
   python3 -m playwright install chromium
   sudo python3 -m playwright install-deps chromium
   
   # Configure credentials
   cp .env.example .env
   nano .env
   ```

3. **Test the setup:**
   ```bash
   python3 test_setup.py
   ```

4. **Run the scraper:**
   ```bash
   python3 daily_scraper.py
   ```

---

## Troubleshooting

### "File not found" errors

Make sure you're in the correct directory:
```bash
cd ~/airr-scraper
pwd  # Should show: /home/yourusername/airr-scraper
ls   # Should list all Python files
```

### Missing airr_sku_rows.csv

This file is **critical** - it contains all 2,968 product codes. Download it from Replit.

### Permission denied

Make scripts executable:
```bash
chmod +x *.py *.sh
```

---

## File Structure

After downloading, your folder should look like this:

```
~/airr-scraper/
├── Core Scripts
│   ├── daily_scraper.py
│   ├── scrape_products_with_cookies.py
│   ├── login_and_save_cookies_.py
│   ├── upload_to_database.py
│   └── clean_all_data.py
│
├── Data Files
│   ├── airr_sku_rows.csv          (2,968 product codes)
│   └── requirements.txt
│
├── Configuration
│   ├── .env.example
│   └── .env                        (you'll create this)
│
├── Setup & Testing
│   ├── ubuntu_setup.sh
│   └── test_setup.py
│
└── Documentation
    ├── UBUNTU_SETUP.md
    ├── DOWNLOAD_GUIDE.md
    ├── CLEAN_AND_RESTART.md
    └── DATABASE_SETUP.md
```

---

**Ready to proceed? See UBUNTU_SETUP.md for complete setup instructions!**
