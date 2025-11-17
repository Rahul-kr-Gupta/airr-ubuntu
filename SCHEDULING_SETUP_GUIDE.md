# Daily Scraping - Scheduling Setup Guide

## ✅ What's Been Configured

1. **Daily Automation Script**: `daily_scraper.py`
   - Automatically runs login → scrape → save workflow
   - Deletes old data before each run
   - Auto-refreshes authentication every 100 products

2. **Deployment Configuration**: Set to "scheduled" mode
   - Ready to run on a schedule
   - Command: `python daily_scraper.py`

## 🕐 Setting Up the 5 PM AEST Schedule

### Step 1: Open Publishing Tool
1. Click on **Tools** in the left sidebar
2. Select **"All tools"** → **"Publishing"**
   - OR type **"Publishing"** in the search bar

### Step 2: Configure Scheduled Deployment
1. In Publishing workspace, select **"Scheduled"** option
2. Click **"Set up your published app"** (or "Edit" if already configured)

### Step 3: Set the Schedule
In the **Schedule** section:

**Option A: Use Natural Language (AI converts to cron)**
- Description: `Daily at 5 PM AEST`
- AI will convert this to cron expression

**Option B: Manual Cron Expression**
- **Cron expression**: `0 7 * * *`
  - This means: 7:00 AM UTC = 5:00 PM AEST (UTC+10)
  - During AEDT (daylight saving UTC+11): `0 6 * * *`
- **Timezone**: Select `Australia/Sydney` or `UTC`

### Step 4: Other Settings
- **Job timeout**: `7200` seconds (2 hours) - gives enough time for all 2,968 products
- **Run command**: Already configured as `python daily_scraper.py`
- **Build command**: Leave empty (not needed)
- **Environment secrets**: Already configured (airr_USERNAME, airr_PASSWORD)

### Step 5: Deploy
1. Click **"Deploy"** or **"Update deployment"**
2. Your scraper will now run automatically every day at 5 PM AEST!

## 📊 What Happens Daily

```
17:00 AEST - Scheduled job starts
├─ 🗑️  Delete old airr_product_data.csv
├─ 🔐 Run login_and_save_cookies_.py
│   └─ Save fresh cookies.json
├─ 🕷️  Run scrape_products_with_cookies.py
│   ├─ Fresh login with new token
│   ├─ Scrape all 2,968 products
│   ├─ Auto-refresh every 100 products
│   └─ Save to airr_product_data.csv
└─ ✅ Complete (~2-3 hours total)
```

## 🧪 Testing Before Scheduling

You can test the daily workflow manually:

```bash
python daily_scraper.py
```

This will:
- Run the complete workflow immediately
- Show you exactly what will happen at 5 PM daily
- Verify everything works before scheduling

## 📁 Output Files

### Daily Output (Overwritten Each Day)
- **airr_product_data.csv** - Fresh product data for current day
  - Format: One row per product-location combination
  - ~30,000 rows, ~1.2 MB
  - Contains all 10 warehouse locations per product

### Temporary Files (Auto-deleted)
- **cookies.json** - Session cookies (refreshed daily)
- **scrape_checkpoint.json** - Resume point (deleted before each run)

## ⚠️ Important Notes

### About AEST vs AEDT
- **AEST** (Australian Eastern Standard Time) = UTC+10
- **AEDT** (Australian Eastern Daylight Time) = UTC+11 (Oct-Apr)

**Recommended**: Use timezone `Australia/Sydney` instead of manual cron so Replit handles daylight saving automatically.

### Monitoring
- Check the Publishing → Scheduled logs to see each daily run
- Logs show complete workflow progress
- Errors are captured and logged

### Manual Runs
You can trigger manual runs anytime:
```bash
python daily_scraper.py
```

This won't affect the scheduled runs.

## 🔧 Troubleshooting

### If scraping fails:
1. Check logs in Publishing workspace
2. Verify airr_USERNAME and airr_PASSWORD secrets are set
3. Run manually: `python daily_scraper.py` to see detailed errors

### If schedule doesn't trigger:
1. Verify deployment is "Active" in Publishing
2. Check timezone setting matches AEST
3. Review cron expression syntax

### If data is incomplete:
- Check logs for errors
- Increase job timeout if needed (currently 2 hours)
- Some products may return 400/500 errors (this is normal)

## 📞 Support

If you need to modify the schedule or workflow:
1. Edit `daily_scraper.py` for workflow changes
2. Update schedule in Publishing → Scheduled settings
3. Re-deploy to apply changes
