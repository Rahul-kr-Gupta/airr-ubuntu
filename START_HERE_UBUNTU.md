# 🚀 START HERE - Ubuntu PC Setup

**Welcome!** This guide will get your AIRR scraper running on Ubuntu in 5 minutes.

---

## 🎯 What This Does

Automatically scrapes **2,968 products** from AIRR website daily:
- 11 warehouse locations per product
- ~30,000 total inventory records
- Saves to CSV + uploads to Supabase database
- Auto-cleans old data before each run
- Perfect for daily automation

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Download Files (2 minutes)

**Easiest method:**
1. In Replit, click **☰ menu** (top left)
2. Select **"Download as zip"**
3. On Ubuntu, extract:
   ```bash
   cd ~/Downloads
   unzip airr-scraper.zip -d ~/airr-scraper
   cd ~/airr-scraper
   ```

**Alternative:** See `UBUNTU_FILES_TO_DOWNLOAD.txt` for file list

### Step 2: Run Automated Setup (2 minutes)

```bash
cd ~/airr-scraper
./ubuntu_setup.sh
```

This installs:
- ✅ Python packages
- ✅ Playwright browser
- ✅ Creates .env config file

### Step 3: Add Your Credentials (1 minute)

```bash
nano .env
```

Fill in:
```bash
airr_USERNAME=your_actual_username
airr_PASSWORD=your_actual_password

SUPABASE_HOST=your_supabase_host
SUPABASE_DBNAME=postgres
SUPABASE_USER=postgres.yourprojectid
SUPABASE_PASSWORD=your_database_password
SUPABASE_PORT=6543
```

Save: `Ctrl+X`, `Y`, `Enter`

### Step 4: Test Everything Works

First, verify .env file is loaded correctly:
```bash
python3 test_env_loading.py
```

Should show: ✅ SUCCESS! All credentials loaded correctly from .env file

Then run full system test:
```bash
python3 test_setup.py
```

Should show: ✅ ALL TESTS PASSED!

**If .env test fails:**
- Check .env file exists: `ls -la .env`
- View .env content: `cat .env`
- Make sure no extra spaces or quotes around values
- Each line should be: `KEY=value` (no spaces around =)

### Step 5: Run the Scraper

```bash
python3 daily_scraper.py
```

**Done!** Wait 2-3 hours for completion.

---

## 📊 What Happens When You Run

```
🧹 CLEANUP (automatic)
  → Deletes old CSV files
  → Deletes checkpoints
  → Drops database table

🔐 AUTHENTICATION
  → Logs into AIRR website
  → Gets fresh cookies & token

🕷️ SCRAPING
  → Scrapes 2,968 products
  → 11 warehouses each
  → Saves to CSV

📤 DATABASE UPLOAD
  → Creates fresh table
  → Uploads ~30,000 rows
  → Creates indexes

✅ COMPLETE!
```

**Result:** Fresh inventory snapshot in CSV + database

---

## ⏰ Daily Automation (Optional)

Run automatically every day at 5 PM:

```bash
crontab -e
```

Add:
```
0 17 * * * cd ~/airr-scraper && python3 daily_scraper.py >> scraper.log 2>&1
```

Check logs:
```bash
tail -f ~/airr-scraper/scraper.log
```

---

## 📖 Documentation

**Start with these:**
- `README_UBUNTU.md` - Quick reference
- `UBUNTU_CHECKLIST.md` - Step-by-step checklist
- `UBUNTU_FILES_TO_DOWNLOAD.txt` - What to download

**Detailed guides:**
- `UBUNTU_SETUP.md` - Complete installation guide
- `DOWNLOAD_GUIDE.md` - Download methods
- `CLEAN_AND_RESTART.md` - How cleanup works
- `DATABASE_SETUP.md` - Database configuration

---

## 🔧 Troubleshooting

### Setup fails?
```bash
# Try manual installation
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
python3 -m playwright install chromium
sudo python3 -m playwright install-deps chromium
```

### Authentication fails?
```bash
# Test login
python3 login_and_save_cookies_.py

# Check credentials
cat .env
```

### Something broken?
```bash
# Run diagnostic
python3 test_setup.py

# Clean and restart
python3 clean_all_data.py
python3 daily_scraper.py
```

---

## 💡 Pro Tips

1. **Test with small dataset first:**
   ```bash
   head -n 6 airr_sku_rows.csv > test.csv
   ```

2. **Run in background:**
   ```bash
   nohup python3 daily_scraper.py > scraper.log 2>&1 &
   ```

3. **Monitor progress:**
   ```bash
   tail -f scraper.log
   ```

4. **Stop if needed:**
   ```bash
   pkill -f daily_scraper
   ```

---

## 📊 Expected Output

After successful run:

**Files:**
- `airr_product_data.csv` (~30,000 rows)
- `cookies.json` (authentication)
- `scraper.log` (execution log)

**Database:**
- Table: `airr_product_availability`
- Rows: ~30,000
- Products: 2,968 unique

**Runtime:** 2-3 hours

---

## ✅ Checklist

- [ ] Downloaded files from Replit
- [ ] Ran `./ubuntu_setup.sh`
- [ ] Configured `.env` with credentials
- [ ] Ran `python3 test_setup.py` (all passed)
- [ ] Ran `python3 daily_scraper.py`
- [ ] Verified CSV output
- [ ] Verified database upload
- [ ] (Optional) Set up cron automation

---

## 🆘 Need Help?

**Quick commands:**
```bash
python3 test_setup.py      # Test installation
python3 daily_scraper.py   # Run scraper
tail -f scraper.log        # View logs
pkill -f daily_scraper     # Stop scraper
```

**Documentation:**
- All guides are in markdown (.md) files
- Read them with: `cat FILENAME.md`
- Or open in text editor

---

## 🎉 You're Ready!

Your scraper is configured to:
- ✅ Run on Ubuntu PC
- ✅ Use `.env` file (not Replit Secrets)
- ✅ Auto-clean old data
- ✅ Upload to Supabase
- ✅ Work with daily cron automation

**Just run:**
```bash
python3 daily_scraper.py
```

**And you're done!** 🚀

---

**Questions? Check:** `README_UBUNTU.md` or `UBUNTU_SETUP.md`
