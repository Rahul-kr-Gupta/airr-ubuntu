#!/usr/bin/env python3
"""
Test script to verify Ubuntu setup is working correctly
"""
import sys
import os

def test_python_version():
    """Test Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def test_imports():
    """Test required package imports"""
    print("\nTesting package imports...")
    packages = [
        ('beautifulsoup4', 'bs4'),
        ('lxml', 'lxml'),
        ('pandas', 'pandas'),
        ('playwright', 'playwright'),
        ('python-dotenv', 'dotenv'),
        ('psycopg2-binary', 'psycopg2')
    ]
    
    all_ok = True
    for package_name, import_name in packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - Run: pip3 install {package_name}")
            all_ok = False
    
    return all_ok

def test_env_file():
    """Test .env file exists and has required variables"""
    print("\nTesting .env configuration...")
    
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  Run: cp .env.example .env")
        return False
    
    print("✓ .env file exists")
    
    # Load .env from script directory
    try:
        from pathlib import Path
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / '.env'
        load_dotenv(dotenv_path=env_path)
    except Exception as e:
        print(f"✗ Could not load .env file: {e}")
        return False
    
    required_vars = [
        'airr_USERNAME',
        'airr_PASSWORD',
        'SUPABASE_HOST',
        'SUPABASE_DBNAME',
        'SUPABASE_USER',
        'SUPABASE_PASSWORD',
        'SUPABASE_PORT'
    ]
    
    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if not value or 'your_' in value.lower() or 'yourproject' in value.lower():
            print(f"✗ {var} - Not configured")
            all_ok = False
        else:
            print(f"✓ {var} - Configured")
    
    return all_ok

def test_required_files():
    """Test required files exist"""
    print("\nTesting required files...")
    
    required_files = [
        'daily_scraper.py',
        'scrape_products_with_cookies.py',
        'login_and_save_cookies_.py',
        'upload_to_database.py',
        'airr_sku_rows.csv',
        'requirements.txt'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - Missing!")
            all_ok = False
    
    return all_ok

def test_playwright():
    """Test Playwright browser installation"""
    print("\nTesting Playwright browser...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to launch browser
            browser = p.chromium.launch(headless=True)
            browser.close()
            print("✓ Playwright Chromium browser installed")
            return True
    except Exception as e:
        print(f"✗ Playwright browser not installed")
        print(f"  Run: python3 -m playwright install chromium")
        return False

def main():
    print("="*60)
    print("AIRR Scraper - Ubuntu Setup Test")
    print("="*60)
    print()
    
    results = {
        'Python Version': test_python_version(),
        'Package Imports': test_imports(),
        'Required Files': test_required_files(),
        'Environment Config': test_env_file(),
        'Playwright Browser': test_playwright()
    }
    
    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("="*60)
    
    if all(results.values()):
        print()
        print("✅ ALL TESTS PASSED!")
        print()
        print("You're ready to run the scraper:")
        print("  python3 daily_scraper.py")
        print()
        return 0
    else:
        print()
        print("❌ SOME TESTS FAILED")
        print()
        print("Please fix the issues above and run this test again:")
        print("  python3 test_setup.py")
        print()
        print("For help, see: UBUNTU_SETUP.md")
        print()
        return 1

if __name__ == '__main__':
    exit(main())
