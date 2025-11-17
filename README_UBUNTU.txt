AIRR Product Scraper - Ubuntu Quick Start
==========================================

AUTOMATIC INSTALLATION (Recommended)
------------------------------------
1. Open terminal in this folder
2. Run: ./install_ubuntu.sh
3. Edit .env file: nano .env (add your username/password)
4. Run: ./run_scraper.sh

That's it! The scraper will run for 2-3 hours.


MANUAL INSTALLATION
-------------------
1. Install dependencies:
   sudo apt update
   sudo apt install python3 python3-pip -y
   pip3 install -r requirements.txt
   python3 -m playwright install chromium
   sudo python3 -m playwright install-deps chromium

2. Set up credentials:
   cp .env.example .env
   nano .env
   (Add your AIRR username and password)

3. Run:
   python3 daily_scraper.py


DAILY AUTOMATION (Optional)
----------------------------
Run automatically at 5 PM every day:

1. crontab -e
2. Add this line:
   0 17 * * * cd ~/airr-scraper && /usr/bin/python3 daily_scraper.py >> ~/airr-scraper/scraper.log 2>&1


OUTPUT FILE
-----------
airr_product_data.csv - Contains all scraped product data
(~30,000 rows, one per product-location combination)


REQUIRED FILES
--------------
✓ daily_scraper.py
✓ scrape_products_with_cookies.py
✓ login_and_save_cookies_.py
✓ airr_sku_rows.csv (your product codes)
✓ requirements.txt
✓ .env (create from .env.example)


TROUBLESHOOTING
---------------
Error: "ModuleNotFoundError"
Fix: pip3 install -r requirements.txt

Error: "Executable doesn't exist"
Fix: python3 -m playwright install chromium

Error: "Credentials not found"
Fix: Create .env file with your username/password

Check logs: tail -f scraper.log


HELP
----
See UBUNTU_SETUP.md for detailed instructions
