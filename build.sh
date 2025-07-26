#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully! Database initialization will happen at startup."
