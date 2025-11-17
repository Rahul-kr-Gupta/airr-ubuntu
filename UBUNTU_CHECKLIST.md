# ✅ Ubuntu Setup Checklist

Use this checklist to ensure your Ubuntu PC is properly configured to run the AIRR scraper.

---

## 📥 Download Phase

- [ ] Downloaded all files from Replit to `~/airr-scraper/`
- [ ] Verified `airr_sku_rows.csv` exists (contains 2,968 product codes)
- [ ] Have all Python scripts (.py files)
- [ ] Have `requirements.txt`
- [ ] Have `.env.example`

**Verify:**
```bash
cd ~/airr-scraper
ls -la
```

---

## 🔧 Installation Phase

- [ ] Python 3.9+ installed
- [ ] pip3 installed
- [ ] Python packages installed
- [ ] Playwright Chromium browser installed
- [ ] Playwright system dependencies installed

**Verify:**
```bash
python3 --version       # Should show 3.9+
pip3 --version          # Should show pip version
python3 test_setup.py   # Should pass all tests
```

**If not installed, run:**
```bash
./ubuntu_setup.sh
```

---

## ⚙️ Configuration Phase

- [ ] Created `.env` file (copied from `.env.example`)
- [ ] Added AIRR username (`airr_USERNAME`)
- [ ] Added AIRR password (`airr_PASSWORD`)
- [ ] Added Supabase host (`SUPABASE_HOST`)
- [ ] Added Supabase database name (`SUPABASE_DBNAME`)
- [ ] Added Supabase user (`SUPABASE_USER`)
- [ ] Added Supabase password (`SUPABASE_PASSWORD`)
- [ ] Added Supabase port (`SUPABASE_PORT`)

**Verify:**
```bash
cat .env  # Should show your credentials (not example values)
```

**Edit if needed:**
```bash
nano .env
```

---

## 🧪 Testing Phase

- [ ] Test setup script passes all checks
- [ ] Authentication test successful
- [ ] Test scrape with 5 products successful (optional)

**Run tests:**
```bash
# Full system test
python3 test_setup.py

# Authentication test
python3 login_and_save_cookies_.py

# Optional: Test with small dataset
head -n 6 airr_sku_rows.csv > test.csv
mv test.csv airr_sku_rows.csv
python3 daily_scraper.py
```

---

## 🚀 Production Run

- [ ] Full scraper run completed successfully
- [ ] CSV file created (`airr_product_data.csv`)
- [ ] Data uploaded to Supabase
- [ ] Verified data in Supabase dashboard

**Run full scraper:**
```bash
python3 daily_scraper.py
```

**Expected:**
- Runtime: 2-3 hours
- Output: ~30,000 rows in CSV
- Database: Data uploaded to Supabase

---

## ⏰ Automation Setup (Optional)

- [ ] Cron job configured for daily 5 PM run
- [ ] Test cron job manually
- [ ] Verify logs are being written

**Setup cron:**
```bash
crontab -e
```

**Add line:**
```
0 17 * * * cd ~/airr-scraper && python3 daily_scraper.py >> scraper.log 2>&1
```

**Verify:**
```bash
crontab -l  # List all cron jobs
```

---

## 📊 Verification Phase

- [ ] Check CSV file exists and has data
- [ ] Check database has data
- [ ] Verify row count (~30,000 rows)
- [ ] Verify all 2,968 products scraped
- [ ] Verify all 11 warehouse locations per product

**Verify CSV:**
```bash
wc -l airr_product_data.csv    # Should show ~30,000
head -n 5 airr_product_data.csv # Should show data
```

**Verify database:**
1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to Table Editor
4. Find `airr_product_availability` table
5. Check row count

**SQL query:**
```sql
SELECT COUNT(*) FROM airr_product_availability;
-- Should show ~30,000

SELECT COUNT(DISTINCT product_code) FROM airr_product_availability;
-- Should show 2,968
```

---

## 🔒 Security Phase

- [ ] `.env` file has restricted permissions
- [ ] `.env` added to `.gitignore`
- [ ] No credentials in git history
- [ ] Credentials stored securely

**Secure .env:**
```bash
chmod 600 .env
echo ".env" >> .gitignore
```

---

## 📝 Documentation Phase

- [ ] Read `UBUNTU_SETUP.md`
- [ ] Read `CLEAN_AND_RESTART.md`
- [ ] Understand how cleanup works
- [ ] Know how to check logs
- [ ] Know how to troubleshoot

---

## 🎯 Final Checklist

- [ ] ✅ Installation complete
- [ ] ✅ Configuration complete
- [ ] ✅ Testing successful
- [ ] ✅ Full scraper run successful
- [ ] ✅ Data verified in CSV and database
- [ ] ✅ Automation configured (optional)
- [ ] ✅ Security measures applied
- [ ] ✅ Documentation reviewed

---

## 🆘 If Something Failed

### Installation Issues

```bash
# Re-run automated setup
./ubuntu_setup.sh

# Or install manually
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
python3 -m playwright install chromium
sudo python3 -m playwright install-deps chromium
```

### Configuration Issues

```bash
# Verify .env file
cat .env

# Edit credentials
nano .env

# Test authentication
python3 login_and_save_cookies_.py
```

### Runtime Issues

```bash
# Check logs
tail -f scraper.log

# Run test setup
python3 test_setup.py

# Clean and restart
python3 clean_all_data.py
python3 daily_scraper.py
```

---

## 📞 Quick Help

| Issue | Command |
|-------|---------|
| Test installation | `python3 test_setup.py` |
| Test authentication | `python3 login_and_save_cookies_.py` |
| Run scraper | `python3 daily_scraper.py` |
| View logs | `tail -f scraper.log` |
| Clean data | `python3 clean_all_data.py` |
| Stop scraper | `pkill -f daily_scraper` |

---

**When all items are checked, you're ready for daily automated scraping!** ✅
