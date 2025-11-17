@echo off
REM Windows Batch Script to Run AIRR Scraper
REM Double-click this file to run the daily scraper

echo ========================================
echo   AIRR Product Scraper - Daily Run
echo ========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Starting daily scraper workflow...
echo.

REM Run the daily scraper
python daily_scraper.py

echo.
echo ========================================
echo   Scraping Complete
echo ========================================
echo.
echo Output saved to: airr_product_data.csv
echo.

pause
