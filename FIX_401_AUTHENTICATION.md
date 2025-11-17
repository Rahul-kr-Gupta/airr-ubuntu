# Fix: "Your login has expired" (HTTP 401) Errors

## Problem
During scheduled execution, the scraper was failing with repeated HTTP 401 errors:
```
[15/2968] Scraping: 10083
✗ Error: HTTP 401: Your login has expired
[16/2968] Scraping: 10088
✗ Error: HTTP 401: Your login has expired
```

**Root Cause**: Authentication tokens expire very quickly (around 15-30 products), but the auto-refresh was only happening every 100 products.

## Solution Applied

### 1. **Increased Refresh Frequency** (10x more frequent)
- **Before**: Refreshed every 100 products
- **After**: Refreshes every **10 products**

```python
refresh_interval=10  # Was 100
```

### 2. **Automatic Retry on 401 Errors**
Added intelligent retry logic that:
- Detects 401 authentication errors
- Immediately refreshes authentication
- Retries the failed product up to 3 times
- Moves on if refresh fails

```python
# Try scraping with automatic retry on 401
max_retries = 2
for attempt in range(max_retries + 1):
    product_data = scrape_product_via_api(page, product_code, token, warehouse)
    
    # If 401 error, refresh auth and retry
    if product_data['scrape_status'] == 'error' and '401' in str(product_data.get('error_message', '')):
        if attempt < max_retries:
            print(f"  🔄 Auth expired, refreshing and retrying...")
            new_token = refresh_authentication(page)
            if new_token:
                token = new_token
                continue  # Retry with new token
```

### 3. **Added Headless Browser Arguments**
Added arguments for better compatibility in scheduled deployment environments:

```python
browser = p.chromium.launch(
    headless=True,
    args=[
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu'
    ]
)
```

## How It Works Now

### Authentication Lifecycle

```
Product 1-10: Use initial token
Product 10: Auto-refresh authentication ✓
Product 11-20: Use refreshed token
Product 20: Auto-refresh authentication ✓
... (continues every 10 products)
```

### When 401 Error Occurs

```
Product 15: HTTP 401 error detected
  ↓
🔄 Immediate refresh authentication
  ↓
Retry Product 15 with new token
  ↓
✓ Success!
```

### Retry Flow

```
Attempt 1: Try with current token
  ↓ (If 401)
🔄 Refresh auth
  ↓
Attempt 2: Try with new token
  ↓ (If 401 again)
🔄 Refresh auth
  ↓
Attempt 3: Try with new token
  ↓ (If still fails)
✗ Give up, move to next product
```

## Expected Behavior

### ✅ Good Output
```
[15/2968] Scraping: 10083
  ✓ Product Name - 10 locations
[20/2968] Scraping: 10088
🔄 Refreshing authentication...
  ✓ Authentication refreshed, new token: eyJhbGciOiJIUzI1NiIs...
  Continuing with refreshed token...
[21/2968] Scraping: 10091
  ✓ Product Name - 10 locations
```

### ⚠️ If 401 Still Occurs (Rare)
```
[15/2968] Scraping: 10083
  ✗ Error: HTTP 401: Your login has expired
  🔄 Auth expired, refreshing and retrying (attempt 2/3)...
  ✓ Authentication refreshed
  ✓ Product Name - 10 locations
```

### ❌ If Refresh Completely Fails (Very Rare)
```
[15/2968] Scraping: 10083
  ✗ Error: HTTP 401: Your login has expired
  🔄 Auth expired, refreshing and retrying (attempt 2/3)...
  ✗ Could not refresh token, skipping retry
  (Product marked as error, scraper continues)
```

## Files Modified

1. **scrape_products_with_cookies.py**
   - Changed `refresh_interval` from 100 to 10
   - Added automatic retry logic for 401 errors
   - Added headless browser arguments
   - Improved token management

2. **login_and_save_cookies_.py**
   - Added automatic browser installation
   - Added headless browser arguments
   - Better error reporting

3. **install_browsers.sh**
   - New build script for scheduled deployments
   - Installs Playwright browsers before each run

## Testing

### Local Test (Quick)
```bash
# Test with first 50 products to verify fix
python scrape_products_with_cookies.py
```

### Scheduled Deployment Test
1. Go to **Publishing** → **Scheduled**
2. Click **"Run now"** to trigger immediate test
3. Watch logs for:
   - `🔄 Refreshing authentication...` (every 10 products)
   - `✓ Authentication refreshed` (successful refreshes)
   - No repeated 401 errors

## Performance Impact

### Before Fix
- ❌ Failed after 15-30 products
- ❌ All subsequent products failed with 401
- ❌ Total failure rate: ~99%

### After Fix
- ✅ Refreshes every 10 products (~300 refreshes total)
- ✅ Auto-retry on any 401 errors
- ✅ Expected success rate: >95%
- ⏱️ Small time overhead: ~2 seconds per refresh = ~10 minutes total

### Total Runtime Estimate
- **Products**: 2,968
- **Base scraping time**: 2-3 hours
- **Auth refreshes**: 300 refreshes × 2 seconds = 10 minutes
- **Total time**: ~2-3.5 hours

## Troubleshooting

### If 401 errors persist:
1. Check that `airr_USERNAME` and `airr_PASSWORD` are set in Deployment Secrets
2. Verify credentials are correct
3. Check if website changed login flow
4. Consider reducing `refresh_interval` to 5 for even more frequent refreshes

### If refresh fails repeatedly:
1. Check logs for error messages during refresh
2. Verify login form selectors haven't changed
3. Test login manually: `python login_and_save_cookies_.py`

### If scraping is too slow:
- Increase `refresh_interval` from 10 to 15 or 20
- Monitor for 401 errors to find sweet spot
- Current setting (10) is conservative/safe

## Summary

**Problem**: Auth expired every 15-30 products, causing 99% failure rate  
**Solution**: Refresh every 10 products + automatic retry on 401  
**Result**: Expected >95% success rate with reliable auto-recovery  

The scraper now proactively refreshes authentication before it expires AND automatically recovers if it does expire.
