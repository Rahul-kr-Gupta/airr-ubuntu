# Testing Scheduled Deployment Fix

## Problem
The scheduled deployment was failing with:
```
❌ FAILED: Could not authenticate. Aborting
```

## Root Cause
Playwright browsers were not installed in the scheduled deployment environment, which is more isolated than the regular Replit workspace.

## Solution Applied

### 1. Updated `login_and_save_cookies_.py`
Added:
- Browser installation check before running
- More robust browser launch arguments for headless environments:
  ```python
  args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  ```
- Better error handling and debugging output
- Proper return codes (True/False) for success/failure

### 2. Created `install_browsers.sh`
Build script that:
- Installs Chromium browser for Playwright
- Installs system dependencies
- Runs before each scheduled deployment

### 3. Updated Deployment Configuration
- **Build command**: `bash install_browsers.sh` (installs browsers before each run)
- **Run command**: `python daily_scraper.py` (executes the workflow)

## Testing the Fix

### Option 1: Test Locally First
```bash
# Test the login script
python login_and_save_cookies_.py

# If successful, test the full workflow
python daily_scraper.py
```

### Option 2: Test in Scheduled Deployment
1. Go to **Publishing** → **Scheduled**
2. Click **"Run now"** or **"Test deployment"** (if available)
3. Check the logs for:
   - "✓ Playwright browsers ready"
   - "✓ Success! Saved authentication data to cookies.json"
   - "✅ DAILY SCRAPING WORKFLOW COMPLETED SUCCESSFULLY"

## What to Check in Deployment Logs

### Good Signs ✅
```
Installing Playwright browsers...
✓ Browser installation complete
Checking Playwright browser installation...
✓ Playwright browsers ready
Starting login process for user: WEBBARRY
Navigating to login page...
Looking for login form...
✓ Success! Saved authentication data to cookies.json
```

### If Still Failing ❌

Check the logs for:

**1. Environment Variables Not Found**
```
Error: Credentials not found in environment variables
```
**Fix**: Add `airr_USERNAME` and `airr_PASSWORD` to Deployment Secrets:
- Go to Publishing → Scheduled → Edit
- Scroll to "Deployment secrets"
- Add both secrets

**2. Timeout Errors**
```
Timeout 60000ms exceeded
```
**Fix**: Network issue or page loading too slow
- Increase timeout in login script
- Check if website is accessible

**3. Browser Launch Errors**
```
Error: browserType.launch
```
**Fix**: Add more browser arguments or use alternative browser binary

## Next Steps

1. **Test the login script manually**:
   ```bash
   python login_and_save_cookies_.py
   ```

2. **If successful, configure the schedule in Publishing**:
   - Schedule: `Daily at 5 PM AEST` → becomes `0 7 * * *` (UTC)
   - Timezone: `Australia/Sydney`
   - Job timeout: `7200` seconds

3. **Deploy and monitor**:
   - Click "Deploy" 
   - Test with "Run now" button
   - Check logs for successful execution

## Troubleshooting Commands

If deployment still fails, add these debug commands to `daily_scraper.py`:

```python
# Check environment
print("Python version:", sys.version)
print("Environment variables:", [k for k in os.environ.keys() if 'airr' in k.lower()])

# Check Playwright
import subprocess
result = subprocess.run(["python", "-m", "playwright", "--version"], capture_output=True, text=True)
print("Playwright version:", result.stdout)
```

## Expected Daily Workflow Duration
- **Build phase**: ~2-3 minutes (install browsers)
- **Login**: ~10-20 seconds
- **Scraping**: ~2-3 hours (2,968 products)
- **Total**: ~2-3 hours

Make sure job timeout is set to at least `7200` seconds (2 hours).
