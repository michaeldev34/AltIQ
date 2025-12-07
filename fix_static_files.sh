#!/bin/bash

# Fix for "Missing staticfiles manifest entry" error on PythonAnywhere

echo "========================================="
echo "Fixing Static Files Issue"
echo "========================================="
echo ""

# Make sure we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
workon altiq-env

# Pull latest changes (includes the settings fix)
echo ""
echo "Pulling latest changes from GitHub..."
git pull origin main

# Check if tailwind.css exists
echo ""
echo "Checking for Tailwind CSS file..."
if [ -f "static/css/tailwind.css" ]; then
    echo "✓ Found static/css/tailwind.css"
    ls -lh static/css/tailwind.css
else
    echo "✗ WARNING: static/css/tailwind.css not found!"
    echo "  You may need to build it locally and push to GitHub, or install Node.js"
fi

# Remove old staticfiles directory
echo ""
echo "Removing old staticfiles directory..."
rm -rf staticfiles

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Verify collection
echo ""
echo "Verifying static files were collected..."
if [ -d "staticfiles/css" ]; then
    echo "✓ Static files collected successfully!"
    echo ""
    echo "CSS files in staticfiles:"
    ls -lh staticfiles/css/
else
    echo "✗ ERROR: staticfiles/css directory not found!"
    echo "  Static file collection may have failed."
fi

echo ""
echo "========================================="
echo "Next Steps:"
echo "========================================="
echo "1. Go to the Web tab in PythonAnywhere"
echo "2. Click the green 'Reload' button"
echo "3. Visit your site: https://michaeldev34.pythonanywhere.com"
echo ""
echo "If you still get errors, check the error log in the Web tab."

