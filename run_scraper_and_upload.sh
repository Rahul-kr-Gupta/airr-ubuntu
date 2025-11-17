#!/bin/bash
# Ubuntu/Linux Shell Script to Run AIRR Scraper + Database Upload
# Run with: ./run_scraper_and_upload.sh

echo "========================================================"
echo "  AIRR Product Scraper + Database Upload Pipeline"
echo "========================================================"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install with: sudo apt install python3 python3-pip"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Please create .env file with your credentials"
    echo "Example: cp .env.example .env && nano .env"
    exit 1
fi

# Check if product codes file exists
if [ ! -f airr_sku_rows.csv ]; then
    echo "ERROR: airr_sku_rows.csv not found"
    echo "Please ensure product codes file is in this directory"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo "Starting scraper and database upload pipeline..."
echo ""
echo "This will:"
echo "  1. Scrape 2,968 products from AIRR website (2-3 hours)"
echo "  2. Upload data to Supabase PostgreSQL database"
echo ""
echo "You can close this terminal and let it run in background."
echo ""

# Run the combined pipeline
python3 scrape_and_upload.py

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "========================================================"
    echo "  ✓ Pipeline Complete - SUCCESS"
    echo "========================================================"
    echo ""
    echo "Data scraped and uploaded to database!"
    
    # Show file size if it exists
    if [ -f airr_product_data.csv ]; then
        FILE_SIZE=$(du -h airr_product_data.csv | cut -f1)
        LINE_COUNT=$(wc -l < airr_product_data.csv)
        echo "CSV file size: $FILE_SIZE"
        echo "CSV rows: $LINE_COUNT"
    fi
else
    echo "========================================================"
    echo "  ✗ Pipeline Failed"
    echo "========================================================"
    echo ""
    echo "Check the error messages above"
    echo "Common issues:"
    echo "  - Check .env credentials (both AIRR and Supabase)"
    echo "  - Run: python3 -m playwright install chromium"
    echo "  - Check internet connection"
    echo "  - Verify database connection settings"
fi

echo ""
