# Running AIRR Scraper Locally on Your PC

## Prerequisites

- **Python 3.9 or higher** (Download from https://www.python.org/downloads/)
- **Internet connection** (for scraping)
- **AIRR account credentials** (username and password)

## Setup Instructions

### 1. Download the Project

Download these files to a folder on your PC:
- `scrape_products_with_cookies.py`
- `login_and_save_cookies_.py`
- `daily_scraper.py`
- `airr_sku_rows.csv` (your product codes file)
- `requirements.txt`
- `.env.example`

### 2. Install Python Dependencies

Open Command Prompt (Windows) or Terminal (Mac/Linux) and navigate to the project folder:

```bash
cd path/to/your/project/folder
```

Install required packages:

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

After installing packages, install the Chromium browser for Playwright:

```bash
python -m playwright install chromium
```

If you encounter issues on Linux, also run:

```bash
python -m playwright install-deps chromium
```

### 4. Configure Credentials

1. Copy `.env.example` to `.env`:
   - **Windows**: `copy .env.example .env`
   - **Mac/Linux**: `cp .env.example .env`

2. Edit `.env` file with your credentials:
   ```
   airr_USERNAME=your_actual_username
   airr_PASSWORD=your_actual_password
   ```

3. Save the file

**Important**: Never share your `.env` file or commit it to version control!

## Running the Scraper

### Option 1: Daily Workflow (Recommended)

Run the complete daily workflow that deletes old data and scrapes fresh:

```bash
python daily_scraper.py
```

This will:
1. Delete old `airr_product_data.csv` (if exists)
2. Login and save cookies
3. Scrape all 2,968 products
4. Save to `airr_product_data.csv`

**Duration**: 2-3 hours for all products

### Option 2: Login Only

Test your credentials and save cookies:

```bash
python login_and_save_cookies_.py
```

### Option 3: Scrape Only (Manual)

Scrape products using existing cookies:

```bash
python scrape_products_with_cookies.py
```

**Note**: You must run login first or have valid `cookies.json`

## Output Files

### Main Output
- **airr_product_data.csv** - Product data with warehouse availability
  - Format: One row per product-location combination
  - ~30,000 rows (2,968 products × 10 locations)

### Temporary Files
- **cookies.json** - Authentication cookies (auto-generated)
- **scrape_checkpoint.json** - Resume point if scraping is interrupted
- **error_screenshot.png** - Screenshot if login fails (for debugging)

## Resuming After Interruption

If scraping stops mid-way:
1. Just run `python daily_scraper.py` or `python scrape_products_with_cookies.py` again
2. It will automatically resume from the last checkpoint
3. To start fresh, delete `scrape_checkpoint.json` first

## Scheduled Automation (Windows)

### Using Task Scheduler

1. Open **Task Scheduler**
2. Click **"Create Basic Task"**
3. Name: `AIRR Daily Scraper`
4. Trigger: **Daily at 5:00 PM**
5. Action: **Start a program**
   - Program: `python`
   - Arguments: `daily_scraper.py`
   - Start in: `C:\path\to\your\project\folder`
6. Click **Finish**

### Using Batch Script

Create `run_scraper.bat`:
```batch
@echo off
cd /d "C:\path\to\your\project\folder"
python daily_scraper.py
pause
```

Double-click to run manually, or schedule this batch file.

## Scheduled Automation (Mac/Linux)

### Using Cron

1. Open terminal and edit crontab:
   ```bash
   crontab -e
   ```

2. Add this line (runs daily at 5 PM):
   ```
   0 17 * * * cd /path/to/your/project && /usr/bin/python3 daily_scraper.py >> scraper.log 2>&1
   ```

3. Save and exit

### Using Shell Script

Create `run_scraper.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 daily_scraper.py
```

Make it executable:
```bash
chmod +x run_scraper.sh
```

Run with: `./run_scraper.sh`

## Troubleshooting

### "ModuleNotFoundError: No module named 'playwright'"
**Fix**: Run `pip install -r requirements.txt`

### "playwright._impl._api_types.Error: Executable doesn't exist"
**Fix**: Run `python -m playwright install chromium`

### "Error: Credentials not found"
**Fix**: Make sure `.env` file exists and has correct credentials

### "Could not authenticate"
**Fix**: 
- Check username/password in `.env`
- Check internet connection
- Try running `python login_and_save_cookies_.py` to see detailed error

### Scraping is slow
**Normal**: Scraping 2,968 products takes 2-3 hours
- Auth refreshes every 10 products (~300 refreshes)
- Small delay between products to avoid overloading server

### "Your login has expired" errors
**Fix**: Script auto-refreshes every 10 products and retries 401 errors
- Should recover automatically
- If persistent, check if credentials changed

## Performance Settings

### Faster Scraping (Less Stable)
Edit `scrape_products_with_cookies.py`, line 415:
```python
refresh_interval=20  # Change from 10 to 20
```

### More Stable (Slower)
```python
refresh_interval=5  # Change from 10 to 5
```

## File Structure

```
your-project-folder/
├── scrape_products_with_cookies.py  (main scraper)
├── login_and_save_cookies_.py       (authentication)
├── daily_scraper.py                 (daily workflow)
├── airr_sku_rows.csv                (product codes - required)
├── requirements.txt                 (dependencies)
├── .env                             (your credentials - create this)
├── .env.example                     (template)
├── cookies.json                     (auto-generated)
├── airr_product_data.csv           (output - auto-generated)
└── scrape_checkpoint.json          (auto-generated)
```

## Tips

1. **Test First**: Run with a small product list to test
   - Edit `airr_sku_rows.csv` to include only 5-10 products
   - Run `python daily_scraper.py`
   - Check output before running full scrape

2. **Monitor Progress**: The script prints progress every product:
   ```
   [1/2968] Scraping: 10002 ✓
   [10/2968] Scraping: 10024
   🔄 Refreshing authentication... ✓
   ```

3. **Check Output**: After completion, open `airr_product_data.csv` in Excel/Google Sheets

4. **Backup Data**: The daily workflow deletes old data, so backup important files first

## System Requirements

- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 10MB for output file
- **Internet**: Stable connection for 2-3 hours
- **Python**: 3.9 or higher

## Support

If you encounter issues:
1. Check the error message carefully
2. Verify `.env` credentials are correct
3. Try running login script alone: `python login_and_save_cookies_.py`
4. Check `error_screenshot.png` if login fails

## Security Notes

- ✅ Keep `.env` file private (contains your password)
- ✅ Never commit `.env` to Git
- ✅ Use strong AIRR account password
- ✅ Run only on trusted computers
