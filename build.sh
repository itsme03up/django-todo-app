#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Checking current migrations..."
python manage.py showmigrations

echo "Running database migrations..."
python manage.py migrate --verbosity=2

echo "Verifying database tables..."
python manage.py shell -c "from django.db import connection; print('Tables:', connection.introspection.table_names())"

echo "Build completed successfully!"
