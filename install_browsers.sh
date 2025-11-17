#!/bin/bash
# Install Playwright browsers for scheduled deployment

echo "Installing Playwright browsers..."
python -m playwright install chromium

echo "Installing system dependencies for Playwright..."
python -m playwright install-deps chromium 2>/dev/null || echo "Some system dependencies may be missing (this is normal in restricted environments)"

echo "✓ Browser installation complete"
