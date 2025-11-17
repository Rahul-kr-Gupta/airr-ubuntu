#!/bin/bash
# Ubuntu Installation Script for AIRR Scraper
# Run this script to set up everything automatically

set -e  # Exit on error

echo "========================================"
echo "  AIRR Scraper - Ubuntu Setup"
echo "========================================"
echo ""

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo "ERROR: This script is for Ubuntu/Debian systems only"
    exit 1
fi

echo "Step 1: Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

echo ""
echo "Step 2: Installing Python packages..."
pip3 install -r requirements.txt

echo ""
echo "Step 3: Installing Playwright browser..."
python3 -m playwright install chromium

echo ""
echo "Step 4: Installing Playwright system dependencies..."
echo "(This may ask for sudo password)"
sudo python3 -m playwright install-deps chromium

echo ""
echo "Step 5: Setting up credentials file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "IMPORTANT: Edit .env file with your credentials:"
    echo "  nano .env"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Make run script executable
chmod +x run_scraper.sh

echo ""
echo "========================================"
echo "  ✓ Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file with your AIRR credentials:"
echo "   nano .env"
echo ""
echo "2. Run the scraper:"
echo "   ./run_scraper.sh"
echo ""
echo "3. (Optional) Set up daily automation:"
echo "   crontab -e"
echo "   Add: 0 17 * * * cd $(pwd) && /usr/bin/python3 daily_scraper.py >> $(pwd)/scraper.log 2>&1"
echo ""
