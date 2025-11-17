# Quick Start - Running on Your PC

## 5-Minute Setup

### Step 1: Install Python
Download and install Python 3.9+ from https://www.python.org/downloads/

### Step 2: Install Dependencies
Open terminal/command prompt in the project folder:
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### Step 3: Add Your Credentials
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your AIRR username and password

### Step 4: Run the Scraper

**Windows**: Double-click `run_scraper.bat`  
**Mac/Linux**: Run `./run_scraper.sh` in terminal  
**Or manually**: `python daily_scraper.py`

### Step 5: Wait
The scraper will run for 2-3 hours and save data to `airr_product_data.csv`

## That's It!

For detailed instructions, see `LOCAL_SETUP.md`

## Files You Need

**Required**:
- `daily_scraper.py`
- `scrape_products_with_cookies.py`
- `login_and_save_cookies_.py`
- `airr_sku_rows.csv` (your product codes)
- `requirements.txt`
- `.env` (create from `.env.example`)

**Optional helpers**:
- `run_scraper.bat` (Windows quick-run)
- `run_scraper.sh` (Mac/Linux quick-run)

## Daily Automation

**Windows**: Use Task Scheduler to run `run_scraper.bat` daily at 5 PM  
**Mac/Linux**: Use cron to run `run_scraper.sh` daily at 5 PM  

See `LOCAL_SETUP.md` for detailed automation setup.
