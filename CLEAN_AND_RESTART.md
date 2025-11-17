# Clean and Restart - Fresh Scrape

## When to Use This

Use this when you want to start a **completely fresh scrape** and remove all old data:

- Starting a new day's scrape
- Testing the scraper
- Had errors and want to restart from scratch
- Want to clear old data from database

## What Gets Cleaned

When you start a fresh scrape, the system automatically cleans:

1. **CSV Files**
   - `airr_product_data.csv` - Previous scraped data
   - `airr_product_data_backup.csv` - Backup files

2. **Checkpoint Files**
   - `scrape_checkpoint.json` - Resume progress
   - Forces scrape to start from product #1

3. **Database Table**
   - Drops `airr_product_availability` table
   - Removes all previous data
   - Table will be recreated on upload

## Automatic Cleanup (Recommended)

The `daily_scraper.py` script **automatically cleans everything** when started:

```bash
python3 daily_scraper.py
```

This will:
1. ✅ Delete old CSV files
2. ✅ Delete checkpoint files
3. ✅ Drop database table
4. ✅ Start fresh scrape from product #1
5. ✅ Upload fresh data to database

## Manual Cleanup

If you want to clean data without running the scraper:

```bash
python3 clean_all_data.py
```

This interactive script will:
- Ask for confirmation
- Show what will be deleted
- Clean CSV files, checkpoints, and database

## Resume vs Fresh Start

### Fresh Start (Default)
```bash
python3 daily_scraper.py
```
- Deletes everything
- Starts from product #1
- Use for daily automated runs

### Resume from Checkpoint
If the scraper crashes mid-run, you can resume:
```bash
# DON'T delete checkpoint file
python3 scrape_products_with_cookies.py
```
- Keeps checkpoint file
- Resumes from last saved position
- Use only for crash recovery

## Database Behavior

### Fresh Daily Run
```
Day 1: Scrape → Upload → Database has Day 1 data
Day 2: Clean → Scrape → Upload → Database has only Day 2 data
Day 3: Clean → Scrape → Upload → Database has only Day 3 data
```

Each daily run **replaces** the previous data with fresh data.

### Keep Historical Data (Future Enhancement)

If you want to keep historical data, modify the cleanup to **not** drop the table:
- Data will accumulate over time
- You can track inventory changes
- Requires more storage

## Quick Commands

**Start fresh scrape (auto cleanup):**
```bash
python3 daily_scraper.py
```

**Manual cleanup only:**
```bash
python3 clean_all_data.py
```

**Check what data exists:**
```bash
# Local files
ls -lh airr_product_data.csv scrape_checkpoint.json

# Database (via psql)
psql $DATABASE_URL -c "SELECT COUNT(*) FROM airr_product_availability"
```

## For Ubuntu/EC2

### Daily Cron Job (Auto-cleanup)
```bash
# Edit crontab
crontab -e

# Add this line for daily 5 PM run
0 17 * * * cd ~/airr-scraper && python3 daily_scraper.py >> scraper.log 2>&1
```

This will automatically:
- Clean old data
- Scrape fresh data
- Upload to database
- Every day at 5 PM

## Safety Note

⚠️ **Database cleanup is permanent!**

Once the database table is dropped, the data cannot be recovered. Make sure you:
- Have backups if needed
- Understand that each daily run replaces previous data
- Export important data before cleanup if needed

## Troubleshooting

**Scraper resumes instead of starting fresh:**
```bash
# Make sure checkpoint is deleted
rm -f scrape_checkpoint.json
python3 daily_scraper.py
```

**Database not cleaned:**
- Check database credentials are set
- Verify connection to Supabase
- Check logs for error messages

**Want to keep old data:**
- Export CSV before running daily_scraper
- Or modify script to skip database cleanup
