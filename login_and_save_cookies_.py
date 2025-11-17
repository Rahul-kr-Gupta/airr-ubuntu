import os
import json
import subprocess
import sys
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
USERNAME = "WEBBARRY"
PASSWORD = "Petfood#123"

def ensure_playwright_browsers():
    """Ensure Playwright browsers are installed"""
    try:
        print("Checking Playwright browser installation...")
        # Try to install browsers if not already installed
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("✓ Playwright browsers ready")
            return True
        else:
            print(f"Warning: Browser installation returned code {result.returncode}")
            print(result.stdout)
            return True  # Continue anyway
    except Exception as e:
        print(f"Warning: Could not install browsers: {e}")
        return True  # Continue anyway, might already be installed

def login_and_save_cookies():
    """
    Log into https://orderonline.airr.com.au/ and save all cookies to a file
    """
    if not USERNAME or not PASSWORD:
        print("Error: Credentials not found in environment variables")
        print("Please ensure airr_USERNAME and airr_PASSWORD are set")
        print(f"Current USERNAME value: {USERNAME}")
        print(f"Available env vars: {list(os.environ.keys())}")
        return False
    
    print(f"Starting login process for user: {USERNAME}")
    
    # Ensure browsers are installed
    ensure_playwright_browsers()
    
    with sync_playwright() as p:
        # Launch browser with more robust settings for scheduled deployments
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Navigate to the login page
            print("Navigating to login page...")
            page.goto('https://orderonline.airr.com.au/', timeout=60000)
            
            # Wait for page to load
            page.wait_for_load_state('networkidle')
            
            # Try to find and fill login form
            # Note: These selectors may need to be adjusted based on the actual page structure
            print("Looking for login form...")
            
            # Wait for username field (adjust selector as needed)
            page.wait_for_selector('input[type="text"], input[name*="user"], input[id*="user"]', timeout=10000)
            
            # Fill in username
            print("Entering username...")
            username_field = page.locator('input[type="text"], input[name*="user"], input[id*="user"]').first
            username_field.fill(USERNAME)
            
            # Fill in password
            print("Entering password...")
            password_field = page.locator('input[type="password"]').first
            password_field.fill(PASSWORD)
            
            # Click login button
            print("Clicking login button...")
            login_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("Login"), button:has-text("Sign in")').first
            login_button.click()
            
            # Wait for navigation after login
            print("Waiting for login to complete...")
            page.wait_for_load_state('networkidle', timeout=30000)
            page.wait_for_timeout(3000)
            
            # Check if login was successful (adjust based on actual behavior)
            current_url = page.url
            print(f"Current URL after login: {current_url}")
            
            # Wait for localStorage to be populated (critical!)
            print("Waiting for localStorage to populate...")
            max_retries = 10
            local_storage = {}
            for i in range(max_retries):
                local_storage = page.evaluate('() => Object.assign({}, window.localStorage)')
                if local_storage and 'token' in local_storage:
                    print(f"✓ localStorage populated with token (attempt {i+1})")
                    break
                page.wait_for_timeout(1000)
            
            if not local_storage or 'token' not in local_storage:
                print("⚠️  Warning: localStorage not populated, trying page refresh...")
                page.reload()
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(2000)
                local_storage = page.evaluate('() => Object.assign({}, window.localStorage)')
            
            # Get all cookies from the browser context
            cookies = context.cookies()
            
            # Get sessionStorage data as well
            session_storage = page.evaluate('() => Object.assign({}, window.sessionStorage)')
            
            # Save all authentication data to a JSON file
            auth_data = {
                'cookies': cookies,
                'localStorage': local_storage,
                'sessionStorage': session_storage,
                'url': current_url
            }
            
            auth_file = 'cookies.json'
            with open(auth_file, 'w') as f:
                json.dump(auth_data, f, indent=2)
            
            print(f"\n✓ Success! Saved authentication data to {auth_file}")
            print(f"\nAuthentication data:")
            print(f"  - Cookies: {len(cookies)}")
            print(f"  - localStorage items: {len(local_storage)}")
            print(f"  - sessionStorage items: {len(session_storage)}")
            
            if local_storage:
                print(f"\nlocalStorage keys: {', '.join(local_storage.keys())}")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Error during login: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            
            try:
                print("\nTaking screenshot for debugging...")
                page.screenshot(path='error_screenshot.png')
                print("Screenshot saved as error_screenshot.png")
            except:
                print("Could not save screenshot")
            
            # Print page content for debugging
            try:
                print("\nPage title:", page.title())
                print("Current URL:", page.url)
                page_content = page.content()
                print(f"Page content (first 500 chars):\n{page_content[:500]}")
            except:
                print("Could not retrieve page info")
            
            return False
            
        finally:
            browser.close()

if __name__ == "__main__":
    success = login_and_save_cookies()
    sys.exit(0 if success else 1)
