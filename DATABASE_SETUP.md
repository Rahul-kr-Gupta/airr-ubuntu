# Database Setup Guide

This guide explains how to upload scraped AIRR product data to your Supabase PostgreSQL database.

## Prerequisites

1. **Supabase Account** - You need a Supabase account with a PostgreSQL database
2. **Database Credentials** - Get your connection details from Supabase
3. **Scraped Data** - Run the scraper first to generate `airr_product_data.csv`

## Quick Start

### 1. Configure Database Credentials

Create a `.env` file with your credentials:

```bash
# Copy the example file
cp .env.example .env

# Edit the file and add your credentials
nano .env
```

Your `.env` file should contain:

```bash
# AIRR Website Credentials
airr_USERNAME=your_airr_username
airr_PASSWORD=your_airr_password

# Supabase PostgreSQL Database Configuration
SUPABASE_HOST=aws-1-ap-south-1.pooler.supabase.com
SUPABASE_DBNAME=postgres
SUPABASE_USER=postgres.odpysbkgdzwcnwkrwrsw
SUPABASE_PASSWORD=IqxEqdiLbFJmEISw
SUPABASE_PORT=6543
```

### 2. Install Database Library (Ubuntu/EC2)

```bash
pip3 install psycopg2-binary
```

### 3. Upload Data to Database

**Option A: Upload existing scraped data**
```bash
python3 upload_to_database.py
```

**Option B: Scrape fresh data AND upload**
```bash
python3 scrape_and_upload.py
```

**Option C: Use Ubuntu shell script**
```bash
chmod +x run_scraper_and_upload.sh
./run_scraper_and_upload.sh
```

## Database Schema

The script automatically creates a table named `airr_product_availability` with the following structure:

```sql
CREATE TABLE airr_product_availability (
    id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL,
    product_name TEXT,
    location_name VARCHAR(100),
    location_abbreviation VARCHAR(20),
    location_id VARCHAR(20),
    qty_available INTEGER DEFAULT 0,
    qty_in_transit INTEGER DEFAULT 0,
    qty_on_hand INTEGER DEFAULT 0,
    qty_on_order INTEGER DEFAULT 0,
    scrape_status VARCHAR(20),
    error_message TEXT,
    scraped_at TIMESTAMP,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_code, location_id, scraped_at)
);
```

### Indexes

The following indexes are automatically created for performance:

- `idx_product_code` - Fast lookups by product code
- `idx_location_id` - Fast lookups by warehouse location
- `idx_scraped_at` - Fast time-based queries

## How It Works

### 1. Upload Process

1. **Read CSV** - Reads data from `airr_product_data.csv`
2. **Create Table** - Creates database table if it doesn't exist
3. **Batch Upload** - Uploads all rows in a single batch operation (fast!)
4. **Handle Duplicates** - Uses `ON CONFLICT` to update existing records
5. **Show Stats** - Displays upload statistics

### 2. Duplicate Handling

The table has a unique constraint on `(product_code, location_id, scraped_at)`. 

- **First run**: All data is inserted
- **Subsequent runs**: Updates existing records with same timestamp, or inserts new records

This allows you to:
- Re-run the upload safely (won't create duplicates)
- Track historical data by scrape date
- Update quantities if you re-scrape the same day

## Usage Examples

### Daily Automated Pipeline

Set up a daily cron job on Ubuntu/EC2:

```bash
# Edit crontab
crontab -e

# Add daily run at 5 PM AEST (7 AM UTC)
0 7 * * * /path/to/run_scraper_and_upload.sh >> /path/to/logs/scraper.log 2>&1
```

### Query the Database

Connect to your database and run queries:

```sql
-- Get latest data for all products
SELECT DISTINCT ON (product_code, location_id)
    product_code, product_name, location_name,
    qty_available, qty_on_hand, scraped_at
FROM airr_product_availability
ORDER BY product_code, location_id, scraped_at DESC;

-- Get products with low stock
SELECT product_code, product_name, location_name, qty_available
FROM airr_product_availability
WHERE scraped_at = (SELECT MAX(scraped_at) FROM airr_product_availability)
  AND qty_available < 10
ORDER BY qty_available;

-- Get total inventory by location
SELECT 
    location_name,
    COUNT(DISTINCT product_code) as total_products,
    SUM(qty_available) as total_qty_available,
    SUM(qty_on_hand) as total_qty_on_hand
FROM airr_product_availability
WHERE scraped_at = (SELECT MAX(scraped_at) FROM airr_product_availability)
GROUP BY location_name
ORDER BY location_name;

-- Track historical changes for a product
SELECT product_code, location_name, qty_available, scraped_at
FROM airr_product_availability
WHERE product_code = '10002'
ORDER BY scraped_at DESC, location_name;
```

## Performance

### Upload Speed

- **~30,000 rows**: Takes 2-5 seconds
- **Batch insert**: Much faster than one-by-one
- **Network**: Depends on your connection to Supabase

### Storage

- **Per day**: ~1.2 MB CSV = ~2-3 MB database
- **Per month**: ~60-90 MB (if run daily)
- **Per year**: ~700 MB - 1 GB

You can periodically archive old data if needed.

## Troubleshooting

### Connection Errors

```
✗ Database error: could not connect to server
```

**Solutions:**
- Check your database credentials in `.env`
- Verify your IP is allowed in Supabase (check IP restrictions)
- Test connection manually:
  ```bash
  psql "postgresql://postgres.odpysbkgdzwcnwkrwrsw:IqxEqdiLbFJmEISw@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
  ```

### SSL Certificate Errors

```
✗ Database error: SSL connection has been closed unexpectedly
```

**Solution:**
- Ensure `sslmode=require` is set in DB_CONFIG
- Update psycopg2: `pip3 install --upgrade psycopg2-binary`

### Permission Errors

```
✗ Database error: permission denied for table
```

**Solution:**
- Verify your database user has CREATE and INSERT permissions
- Check Supabase dashboard → Database → Roles

### CSV File Not Found

```
✗ Error: CSV file 'airr_product_data.csv' not found
```

**Solution:**
- Run the scraper first: `python3 daily_scraper.py`
- Or run combined pipeline: `python3 scrape_and_upload.py`

## Files

- **upload_to_database.py** - Standalone database upload script
- **scrape_and_upload.py** - Combined scraper + upload pipeline
- **run_scraper_and_upload.sh** - Ubuntu shell script for automation
- **.env** - Database credentials (create from .env.example)

## Security Notes

⚠️ **IMPORTANT**: Never commit `.env` file to git!

The `.env` file contains sensitive credentials. The file is already in `.gitignore` to prevent accidental commits.

For Ubuntu/EC2 deployment:
1. Copy `.env.example` to `.env` on your server
2. Fill in real credentials
3. Set proper file permissions: `chmod 600 .env`

## Next Steps

1. ✅ Set up database credentials in `.env`
2. ✅ Run test upload: `python3 upload_to_database.py`
3. ✅ Verify data in Supabase dashboard
4. ✅ Set up daily automation with cron
5. ✅ Create queries/dashboards for your data

Your AIRR product data is now automatically synced to your database! 🎉
