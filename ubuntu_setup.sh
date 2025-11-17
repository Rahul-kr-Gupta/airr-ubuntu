#!/bin/bash
# ==============================================================================
# AIRR Scraper - Ubuntu Setup Script
# ==============================================================================

echo "=============================================================="
echo "AIRR Scraper - Automated Setup for Ubuntu"
echo "=============================================================="
echo ""

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo "❌ This script is for Ubuntu/Debian systems only"
    exit 1
fi

# Step 1: Update system
echo "📦 Step 1: Updating system packages..."
sudo apt update

# Step 2: Install Python
echo ""
echo "🐍 Step 2: Installing Python 3 and pip..."
sudo apt install python3 python3-pip python3-venv -y

# Verify Python installation
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python version: $(python3 --version)"
echo "✓ pip version: $(pip3 --version | cut -d' ' -f2)"

# Step 3: Install Python dependencies
echo ""
echo "📚 Step 3: Installing Python dependencies..."
pip3 install -r requirements.txt

# Step 4: Install Playwright browser
echo ""
echo "🌐 Step 4: Installing Playwright Chromium browser..."
python3 -m playwright install chromium

echo ""
echo "🔧 Step 5: Installing Playwright system dependencies..."
echo "(This may require sudo password)"
sudo python3 -m playwright install-deps chromium

# Step 6: Set up configuration file
echo ""
echo "⚙️  Step 6: Setting up configuration..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env file from template"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env file with your credentials:"
        echo "   nano .env"
        echo ""
        echo "   You need to fill in:"
        echo "   - airr_USERNAME (your AIRR login)"
        echo "   - airr_PASSWORD (your AIRR password)"
        echo "   - SUPABASE_* (your database credentials)"
    else
        echo "❌ .env.example not found"
        exit 1
    fi
else
    echo "✓ .env file already exists"
fi

# Step 7: Make scripts executable
echo ""
echo "🔐 Step 7: Making scripts executable..."
chmod +x *.py
chmod +x *.sh
echo "✓ Scripts are now executable"

# Summary
echo ""
echo "=============================================================="
echo "✅ SETUP COMPLETE!"
echo "=============================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit your credentials:"
echo "   nano .env"
echo ""
echo "2. Test authentication:"
echo "   python3 login_and_save_cookies_.py"
echo ""
echo "3. Run the scraper:"
echo "   python3 daily_scraper.py"
echo ""
echo "4. Set up daily automation (optional):"
echo "   crontab -e"
echo "   Add: 0 17 * * * cd $(pwd) && python3 daily_scraper.py >> scraper.log 2>&1"
echo ""
echo "=============================================================="
echo "For help, see: UBUNTU_SETUP.md"
echo "=============================================================="

