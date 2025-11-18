import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load environment variables from .env file in script directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Debug: Check if .env was loaded
if not os.getenv('SUPABASE_HOST'):
    print(f"⚠️  WARNING: .env file not found or empty!")
    print(f"   Expected location: {env_path.absolute()}")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   Please ensure .env file exists with all credentials\n")

# Force unbuffered output for real-time logs
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

def load_auth_data(auth_file='cookies.json'):
    """Load authentication data from JSON file"""
    try:
        with open(auth_file, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return {'cookies': data, 'localStorage': {}, 'sessionStorage': {}}
            else:
                return data
    except FileNotFoundError:
        print(f"Error: {auth_file} not found. Please run login script first.")
        return None

def load_product_codes(csv_file='airr_sku_rows.csv'):
    """Load product codes from CSV file"""
    try:
        df = pd.read_csv(csv_file)
        product_codes = df['Product code'].astype(str).tolist()
        product_codes = [code.replace('.0', '') if code.endswith('.0') else code for code in product_codes]
        print(f"Loaded {len(product_codes)} product codes from {csv_file}")
        return product_codes
    except Exception as e:
        print(f"Error loading product codes: {e}")
        return []

def refresh_authentication(page):
    """Refresh authentication by re-logging in"""
    print("\n🔄 Refreshing authentication...")
    try:
        USERNAME = os.getenv('airr_USERNAME')
        PASSWORD = os.getenv('airr_PASSWORD')
        
        if not USERNAME or not PASSWORD:
            print("  ✗ Credentials not found")
            return False
        
        page.goto('https://orderonline.airr.com.au/', timeout=30000)
        page.wait_for_timeout(2000)
        
        username_field = page.locator('input[type="text"], input[name*="user"], input[id*="user"]').first
        username_field.fill(USERNAME)
        
        password_field = page.locator('input[type="password"]').first
        password_field.fill(PASSWORD)
        
        login_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("Login")').first
        login_button.click()
        
        page.wait_for_load_state('networkidle', timeout=30000)
        page.wait_for_timeout(2000)
        
        # Update token after refresh
        new_token = page.evaluate('() => localStorage.getItem("token")')
        if new_token:
            try:
                if new_token.startswith('"') and new_token.endswith('"'):
                    new_token = json.loads(new_token)
            except:
                pass
            print(f"  ✓ Authentication refreshed, new token: {new_token[:20]}...")
            return new_token
        
        print("  ✓ Authentication refreshed successfully")
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to refresh: {str(e)[:100]}")
        return False

def scrape_product_via_api(page, product_code, token, warehouse='SYD', max_retries=3):
    """Scrape product using the search API endpoint"""
    product_data = {
        'product_code': product_code,
        'product_name': None,
        'availability_locations': [],
        'scrape_status': 'pending',
        'error_message': None
    }
    
    try:
        # Use the search API endpoint (POST request)
        api_url = f"https://api.orderonline.airr.com.au/search?token={token}&warehouse={warehouse}&page=1&size=20&isElders=false"
        search_data = json.dumps({"search": product_code})
        
        # Use page.evaluate to fetch from within the page context
        result = page.evaluate(f"""
            async () => {{
                try {{
                    const response = await fetch('{api_url}', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json;charset=UTF-8',
                            'Accept': 'application/json, text/plain, */*'
                        }},
                        body: '{search_data}'
                    }});
                    const status = response.status;
                    
                    if (status === 200) {{
                        const data = await response.json();
                        return {{ success: true, data: data }};
                    }} else {{
                        const errorText = await response.text();
                        try {{
                            const errorJson = JSON.parse(errorText);
                            return {{ success: false, status: status, error: errorJson.error || errorText }};
                        }} catch {{
                            return {{ success: false, status: status, error: errorText.substring(0, 100) }};
                        }}
                    }}
                }} catch (e) {{
                    return {{ success: false, error: e.message }};
                }}
            }}
        """)
        
        if not result or not result.get('success'):
            error_msg = result.get('error', 'Unknown error') if result else 'No response'
            status = result.get('status', 'N/A') if result else 'N/A'
            raise Exception(f"HTTP {status}: {error_msg}")
        
        # Extract data from successful response
        data = result.get('data', {})
        if not data:
            raise Exception("No data in response")
        
        # Search API returns an array of products directly
        products = data if isinstance(data, list) else [data]
        
        if not products or len(products) == 0:
            raise Exception("No products found in search results")
        
        # Get the first matching product (should be exact match for product code)
        first_product = products[0]
        
        # Extract product name
        product_data['product_name'] = first_product.get('Description') or first_product.get('FullDescription1')
        
        # Collect all warehouse locations
        all_locations = []
        
        # Add current warehouse from 'Availability'
        current_warehouse = first_product.get('Availability')
        if current_warehouse:
            all_locations.append(current_warehouse)
        
        # Add all other warehouses from 'AvailabilityOther'
        other_warehouses = first_product.get('AvailabilityOther', [])
        if isinstance(other_warehouses, list):
            all_locations.extend(other_warehouses)
        
        # Extract data from each location
        for location in all_locations:
            if not location:
                continue
            location_data = {
                'location_name': location.get('DESCRIPTION', ''),
                'location_abbreviation': location.get('Abbreviation', ''),
                'location_id': location.get('LocationID', ''),
                'qty_available': location.get('QtyAvail', 0),
                'qty_in_transit': location.get('QtyInTransit', 0),
                'qty_on_hand': location.get('QtyOnHand', 0),
                'qty_on_order': location.get('QtyOnOrder', 0)
            }
            product_data['availability_locations'].append(location_data)
        
        product_data['scrape_status'] = 'success'
        locations_count = len(product_data['availability_locations'])
        print(f"  ✓ {product_data['product_name'] or product_code} - {locations_count} locations")
        
    except Exception as e:
        product_data['scrape_status'] = 'error'
        product_data['error_message'] = str(e)[:200]
        print(f"  ✗ Error: {str(e)[:100]}")
    
    return product_data

def scrape_all_products(product_codes, auth_data, output_file='airr_product_data.csv', 
                        checkpoint_file='scrape_checkpoint.json', batch_size=50, refresh_interval=100):
    """Scrape all products with auto-refresh and checkpoint/resume"""
    print(f"\n{'='*60}")
    print(f"Starting product scraping session")
    print(f"Total products: {len(product_codes)}")
    print(f"Output file: {output_file}")
    print(f"Auth refresh: every {refresh_interval} products")
    print(f"{'='*60}\n")
    
    scraped_data = []
    start_index = 0
    
    # Load checkpoint if exists
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                start_index = checkpoint.get('last_index', 0) + 1
                print(f"Resuming from checkpoint at product #{start_index}")
        except:
            pass
    
    # Parse token from localStorage
    token_raw = auth_data.get('localStorage', {}).get('token')
    if not token_raw:
        print("✗ No token found in authentication data!")
        return []
    
    try:
        if token_raw.startswith('"') and token_raw.endswith('"'):
            token = json.loads(token_raw)
        else:
            token = token_raw
    except:
        token = token_raw
    
    # Parse warehouse
    warehouse_raw = auth_data.get('localStorage', {}).get('currentWarehouse', 'SYD')
    try:
        warehouse_data = json.loads(warehouse_raw) if isinstance(warehouse_raw, str) else warehouse_raw
        if isinstance(warehouse_data, dict):
            warehouse = warehouse_data.get('LocationID', 'SYD')
        else:
            warehouse = warehouse_data
    except:
        warehouse = 'SYD'
    
    print(f"Using warehouse: {warehouse}")
    print(f"Initial token: {token[:20] if len(token) > 20 else token}...\n")
    
    # Initialize database connection for live updates
    db_conn = init_database()
    
    with sync_playwright() as p:
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
        
        cookies = auth_data.get('cookies', [])
        if cookies:
            context.add_cookies(cookies)
        
        page = context.new_page()
        
        try:
            # Perform fresh login to get active token
            print("Performing fresh login...")
            USERNAME = os.getenv('airr_USERNAME')
            PASSWORD = os.getenv('airr_PASSWORD')
            
            if not USERNAME or not PASSWORD:
                print("✗ Credentials not found!")
                return []
            
            page.goto('https://orderonline.airr.com.au/', timeout=30000)
            page.wait_for_timeout(2000)
            
            # Fill login form
            username_field = page.locator('input[type="text"], input[name*="user"], input[id*="user"]').first
            username_field.fill(USERNAME)
            
            password_field = page.locator('input[type="password"]').first
            password_field.fill(PASSWORD)
            
            login_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("Login")').first
            login_button.click()
            
            page.wait_for_load_state('networkidle', timeout=30000)
            page.wait_for_timeout(3000)
            
            # Extract fresh token from localStorage
            fresh_token = page.evaluate('() => localStorage.getItem("token")')
            if fresh_token:
                try:
                    if fresh_token.startswith('"') and fresh_token.endswith('"'):
                        token = json.loads(fresh_token)
                    else:
                        token = fresh_token
                except:
                    token = fresh_token
                
                print(f"✓ Fresh login successful!")
                print(f"  New token: {token[:20]}...\n")
            else:
                print("✗ Could not get fresh token!")
                return []
            
            # Scrape all products
            for index, product_code in enumerate(product_codes[start_index:], start=start_index):
                # Auto-refresh authentication every N products
                if index > 0 and index % refresh_interval == 0:
                    new_token = refresh_authentication(page)
                    if new_token and isinstance(new_token, str):
                        token = new_token
                        print(f"  Continuing with refreshed token...\n")
                    else:
                        print("  ⚠ Warning: Could not refresh token, using existing one...\n")
                
                print(f"[{index + 1}/{len(product_codes)}] Scraping: {product_code}")
                
                # Try scraping with automatic retry on 401
                max_retries = 2
                product_data = None
                for attempt in range(max_retries + 1):
                    product_data = scrape_product_via_api(page, product_code, token, warehouse)
                    
                    # If 401 error, refresh auth and retry
                    if product_data['scrape_status'] == 'error' and '401' in str(product_data.get('error_message', '')):
                        if attempt < max_retries:
                            print(f"  🔄 Auth expired, refreshing and retrying (attempt {attempt + 2}/{max_retries + 1})...")
                            new_token = refresh_authentication(page)
                            if new_token and isinstance(new_token, str):
                                token = new_token
                                continue  # Retry with new token
                            else:
                                print(f"  ✗ Could not refresh token, skipping retry")
                                break
                        else:
                            print(f"  ✗ Max retries reached, giving up on this product")
                    else:
                        # Success or non-401 error, move on
                        break
                
                if product_data:
                    scraped_data.append(product_data)
                    
                    # Upload to database in real-time
                    upload_to_database_realtime(db_conn, product_data)
                
                # Save checkpoint every batch_size products
                if (index + 1) % batch_size == 0:
                    save_results(scraped_data, output_file, start_index)
                    
                    with open(checkpoint_file, 'w') as f:
                        json.dump({'last_index': index, 'timestamp': datetime.now().isoformat()}, f)
                    
                    print(f"\n✓ Checkpoint saved at product #{index + 1}")
                    print(f"  Progress: {((index + 1) / len(product_codes)) * 100:.1f}%\n")
                
                time.sleep(0.3)  # Small delay between requests
            
            # Final save
            save_results(scraped_data, output_file, start_index)
            
            # Remove checkpoint file when complete
            if os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)
            
            print(f"\n{'='*60}")
            print(f"Scraping completed!")
            print(f"Total products processed: {len(scraped_data)}")
            print(f"Results saved to: {output_file}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"\n✗ Fatal error: {e}")
            save_results(scraped_data, output_file, start_index)
            print(f"Partial results saved to: {output_file}")
            
        finally:
            browser.close()
            # Close database connection
            if db_conn:
                try:
                    db_conn.close()
                    print("\n✓ Database connection closed")
                except:
                    pass
    
    return scraped_data

def init_database():
    """Initialize database connection and create table if needed"""
    try:
        DB_CONFIG = {
            'host': os.getenv('SUPABASE_HOST'),
            'dbname': os.getenv('SUPABASE_DBNAME'),
            'user': os.getenv('SUPABASE_USER'),
            'password': os.getenv('SUPABASE_PASSWORD'),
            'port': os.getenv('SUPABASE_PORT'),
            'sslmode': 'require'
        }
        
        # Check if credentials are available
        if not all(DB_CONFIG.values()):
            print("⚠️  Database credentials not found - skipping live database updates")
            return None
        
        conn = psycopg2.connect(**DB_CONFIG)
        
        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS airr_product_availability (
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
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_product_code ON airr_product_availability(product_code);
        CREATE INDEX IF NOT EXISTS idx_location_id ON airr_product_availability(location_id);
        CREATE INDEX IF NOT EXISTS idx_scraped_at ON airr_product_availability(scraped_at);
        """
        
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()
        
        print("✓ Database connected - live updates enabled\n")
        return conn
        
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   Continuing with CSV-only mode...\n")
        return None

def upload_to_database_realtime(db_conn, product_data):
    """Upload a single product's data to database immediately"""
    if not db_conn:
        return  # Skip if no database connection
    
    try:
        scraped_at = datetime.now()
        rows_to_insert = []
        
        # Process all warehouse locations for this product
        if product_data['availability_locations']:
            for location in product_data['availability_locations']:
                row = (
                    product_data['product_code'],
                    product_data['product_name'],
                    location.get('location_name'),
                    location.get('location_abbreviation'),
                    location.get('location_id'),
                    int(location.get('qty_available', 0)) if location.get('qty_available') else 0,
                    int(location.get('qty_in_transit', 0)) if location.get('qty_in_transit') else 0,
                    int(location.get('qty_on_hand', 0)) if location.get('qty_on_hand') else 0,
                    int(location.get('qty_on_order', 0)) if location.get('qty_on_order') else 0,
                    product_data['scrape_status'],
                    product_data.get('error_message'),
                    scraped_at
                )
                rows_to_insert.append(row)
        else:
            # No locations - insert single row
            row = (
                product_data['product_code'],
                product_data['product_name'],
                None, None, None, None, None, None, None,
                product_data['scrape_status'],
                product_data.get('error_message'),
                scraped_at
            )
            rows_to_insert.append(row)
        
        # Insert all rows for this product
        insert_query = """
        INSERT INTO airr_product_availability 
        (product_code, product_name, location_name, location_abbreviation, location_id,
         qty_available, qty_in_transit, qty_on_hand, qty_on_order,
         scrape_status, error_message, scraped_at)
        VALUES %s
        """
        
        with db_conn.cursor() as cur:
            execute_values(cur, insert_query, rows_to_insert)
            db_conn.commit()
        
        print(f"    💾 Pushed {len(rows_to_insert)} rows to database")
        
    except Exception as e:
        print(f"    ⚠️  Database upload failed: {e}")
        # Don't fail the scrape if database upload fails

def save_results(scraped_data, output_file, start_index=0):
    """Save scraped data to CSV - one row per product-location"""
    if not scraped_data:
        return
    
    flattened_rows = []
    
    for item in scraped_data:
        if item['availability_locations']:
            # One row per location
            for location in item['availability_locations']:
                row = {
                    'product_code': item['product_code'],
                    'product_name': item['product_name'],
                    'location_name': location.get('location_name'),
                    'location_abbreviation': location.get('location_abbreviation'),
                    'location_id': location.get('location_id'),
                    'qty_available': location.get('qty_available'),
                    'qty_in_transit': location.get('qty_in_transit'),
                    'qty_on_hand': location.get('qty_on_hand'),
                    'qty_on_order': location.get('qty_on_order'),
                    'scrape_status': item['scrape_status'],
                    'error_message': item['error_message']
                }
                flattened_rows.append(row)
        else:
            # No locations found - single row
            row = {
                'product_code': item['product_code'],
                'product_name': item['product_name'],
                'location_name': None,
                'location_abbreviation': None,
                'location_id': None,
                'qty_available': None,
                'qty_in_transit': None,
                'qty_on_hand': None,
                'qty_on_order': None,
                'scrape_status': item['scrape_status'],
                'error_message': item['error_message']
            }
            flattened_rows.append(row)
    
    df = pd.DataFrame(flattened_rows)
    
    # Append to existing file if resuming, otherwise create new
    if start_index > 0 and os.path.exists(output_file):
        df.to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8')
    else:
        df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"  Saved {len(flattened_rows)} rows ({len(scraped_data)} products) to {output_file}")

def main():
    """Main execution"""
    print("Loading authentication data...")
    auth_data = load_auth_data('cookies.json')
    if not auth_data:
        return
    
    cookies_count = len(auth_data.get('cookies', []))
    ls_count = len(auth_data.get('localStorage', {}))
    print(f"✓ Loaded: {cookies_count} cookies, {ls_count} localStorage items\n")
    
    print("Loading product codes...")
    product_codes = load_product_codes('airr_sku_rows.csv')
    if not product_codes:
        return
    
    scraped_data = scrape_all_products(
        product_codes=product_codes,
        auth_data=auth_data,
        output_file='airr_product_data.csv',
        checkpoint_file='scrape_checkpoint.json',
        batch_size=50,
        refresh_interval=10  # Refresh auth every 10 products (more frequent due to short token expiry)
    )
    
    if scraped_data:
        success_count = sum(1 for item in scraped_data if item['scrape_status'] == 'success')
        error_count = sum(1 for item in scraped_data if item['scrape_status'] == 'error')
        total_locations = sum(len(item['availability_locations']) for item in scraped_data)
        
        print("\nSummary:")
        print(f"  Successful: {success_count}")
        print(f"  Errors: {error_count}")
        print(f"  Total products: {len(scraped_data)}")
        print(f"  Total location records: {total_locations}")

if __name__ == "__main__":
    main()
