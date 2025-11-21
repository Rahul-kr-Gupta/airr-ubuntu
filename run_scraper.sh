#!/bin/bash
# Ubuntu/Linux Shell Script to Run AIRR Scraper
# Run with: ./run_scraper.sh

echo "========================================"
echo "  AIRR Product Scraper - Daily Run"
echo "========================================"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

source venv/bin/activate

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
echo "Starting daily scraper workflow..."
echo ""
echo "This will take 2-3 hours to complete."
echo "You can close this terminal and let it run in background."
echo ""

# Run the daily scraper
python3 daily_scraper.py

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "========================================"
    echo "  ✓ Scraping Complete - SUCCESS"
    echo "========================================"
    echo ""
    echo "Output saved to: airr_product_data.csv"
    
    # Show file size if it exists
    if [ -f airr_product_data.csv ]; then
        FILE_SIZE=$(du -h airr_product_data.csv | cut -f1)
        LINE_COUNT=$(wc -l < airr_product_data.csv)
        echo "File size: $FILE_SIZE"
        echo "Total rows: $LINE_COUNT"
    fi
else
    echo "========================================"
    echo "  ✗ Scraping Failed"
    echo "========================================"
    echo ""
    echo "Check the error messages above"
    echo "Common issues:"
    echo "  - Check .env credentials are correct"
    echo "  - Run: python3 -m playwright install chromium"
    echo "  - Check internet connection"
fi

echo ""
