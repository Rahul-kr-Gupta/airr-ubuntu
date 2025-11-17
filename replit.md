# AIRR Product Scraper

## Overview
This project automates the process of logging into https://orderonline.airr.com.au/ and scraping product details for thousands of product codes. The system captures comprehensive product information including prices, availability by location, descriptions, and stock status.

## Project Structure
- `login_and_save_cookies_.py` - Authentication script that logs in and saves session data
- `scrape_products_with_cookies.py` - Main scraping script that extracts product details
- `airr_sku_rows.csv` - Input file with 2970 product codes to scrape
- `cookies.json` - Authentication data (cookies + localStorage) - gitignored for security
- `scraped_products.csv` - Output file with all scraped product data - gitignored
- `scrape_checkpoint.json` - Checkpoint file for resume capability - gitignored

## Features

### Authentication System
- Automatically logs into AIRR portal using secure credentials
- Captures cookies AND localStorage data (critical for this site!)
- Session data includes: token, user info, warehouse settings
- Saves complete authentication state for reuse

### Product Scraping
- Processes 2970 product codes from CSV file
- Extracts: product name, price, availability, stock status, descriptions, images
- Tracks availability by location (Local, Other locations, Branch)
- Checkpoint system: saves progress every 50 products
- Resume capability: if interrupted, resumes from last checkpoint
- Rate limiting: 1 second delay between products to be respectful to server

### Data Captured per Product
- Product Code
- Product Name
- Price (ex GST)
- Overall Availability
- Stock Status (In Stock / Out of Stock)
- Location-specific availability (Local, Other, Branch)
- Product Description
- Category / Brand (if available)
- Image URL

## How to Use

### Step 1: Refresh Login (if needed)
If cookies expire or you need fresh authentication:
```bash
python login_and_save_cookies_.py
```

This will:
- Log into AIRR portal
- Save cookies and localStorage to `cookies.json`
- Display authentication data summary

### Step 2: Run the Scraper
To scrape all 2970 products:
```bash
python scrape_products_with_cookies.py
```

This will:
- Load authentication data from `cookies.json`
- Load product codes from `airr_sku_rows.csv`
- Scrape each product systematically
- Save progress every 50 products
- Generate `scraped_products.csv` with all results

**Note**: Scraping 2970 products will take approximately 1-2 hours due to rate limiting.

### Step 3: View Results
After completion, check `scraped_products.csv` for:
- All product details in structured CSV format
- Success/failure status for each product
- Summary statistics (successful, not found, errors)

## Checkpoint & Resume
The scraper automatically saves progress:
- Progress saved every 50 products
- If interrupted, simply run the script again
- It will automatically resume from the last checkpoint
- Delete `scrape_checkpoint.json` to start fresh

## Credentials
Securely stored in Replit Secrets:
- `airr_USERNAME` - WEBBARRY
- `airr_PASSWORD` - Petfood#123

## Dependencies
- Python 3.11
- Playwright (with Chromium browser)
- BeautifulSoup4
- pandas
- lxml
- python-dotenv
- System libraries for browser support

## Updates & Improvements

### Auto-Refresh Authentication (NEW)
- **Automatic session refresh every 100 products** to prevent authentication timeout
- No more "cookies expired" errors during long scraping sessions
- Seamlessly continues scraping after refresh

### Enhanced Warehouse Data Extraction
- Extracts availability from ALL warehouse locations (not just local)
- Captures location names and quantities for each warehouse
- Data saved in flat CSV format: one row per product-location combination

### Output Format
The CSV file contains:
- product_code - The product SKU
- product_name - Product description
- price - Product price
- location_name - Warehouse location (Sydney, Melbourne, Brisbane, etc.)
- qty_available - Quantity available at that location
- scrape_status - success/error
- error_message - Any error details

## Recent Changes
- **Oct 31, 2025**: Added daily scheduled automation - runs at 5 PM AEST automatically
- **Oct 31, 2025**: Added auto-refresh auth every 100 products + enhanced warehouse data extraction
- **Oct 31, 2025**: Added product scraping functionality with localStorage authentication  
- **Oct 31, 2025**: Initial project setup with Playwright-based login automation

## Daily Automation Schedule

### What Happens Daily at 5:00 PM AEST
The system automatically:
1. 🔐 **Authenticates** - Logs in and gets fresh cookies/token
2. 🕷️ **Scrapes** - Extracts all 2,968 products with warehouse availability
3. 💾 **Saves** - Overwrites airr_product_data.csv with today's fresh data

### Auto-Refresh Feature
- Automatically refreshes authentication every 100 products
- Prevents session expiration during long scraping sessions
- No manual intervention required

### Data Freshness
- Old data is automatically deleted before each run
- Each day gets completely fresh data from the website
- CSV file contains only today's data (not cumulative)
