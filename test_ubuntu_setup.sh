#!/bin/bash
# Quick test script for Ubuntu setup

echo "Testing Ubuntu setup..."
echo ""

# Test Python
if command -v python3 &> /dev/null; then
    echo "✓ Python 3: $(python3 --version)"
else
    echo "✗ Python 3 not found"
    echo "  Install: sudo apt install python3 python3-pip"
fi

# Test pip
if command -v pip3 &> /dev/null; then
    echo "✓ pip3: $(pip3 --version | head -1)"
else
    echo "✗ pip3 not found"
fi

# Test if requirements are installed
echo ""
echo "Checking Python packages..."
python3 -c "import playwright; print('✓ playwright installed')" 2>/dev/null || echo "✗ playwright not installed (run: pip3 install -r requirements.txt)"
python3 -c "import pandas; print('✓ pandas installed')" 2>/dev/null || echo "✗ pandas not installed"
python3 -c "import dotenv; print('✓ python-dotenv installed')" 2>/dev/null || echo "✗ python-dotenv not installed"

# Check .env file
echo ""
if [ -f .env ]; then
    echo "✓ .env file exists"
    if grep -q "your_username_here" .env; then
        echo "  ⚠ Warning: .env still has example values, please edit it"
    fi
else
    echo "✗ .env file not found (copy from .env.example)"
fi

# Check product codes file
if [ -f airr_sku_rows.csv ]; then
    LINES=$(wc -l < airr_sku_rows.csv)
    echo "✓ airr_sku_rows.csv exists ($LINES products)"
else
    echo "✗ airr_sku_rows.csv not found"
fi

# Check scripts
echo ""
echo "Checking scripts..."
[ -f daily_scraper.py ] && echo "✓ daily_scraper.py" || echo "✗ daily_scraper.py missing"
[ -f scrape_products_with_cookies.py ] && echo "✓ scrape_products_with_cookies.py" || echo "✗ scrape_products_with_cookies.py missing"
[ -f login_and_save_cookies_.py ] && echo "✓ login_and_save_cookies_.py" || echo "✗ login_and_save_cookies_.py missing"

echo ""
echo "Setup check complete!"
