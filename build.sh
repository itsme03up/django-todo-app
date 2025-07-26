#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py makemigrations --dry-run --verbosity=2
python manage.py migrate --verbosity=2

echo "Build completed successfully!"
