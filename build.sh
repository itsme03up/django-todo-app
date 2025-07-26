#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo "Creating database if it doesn't exist..."
python manage.py migrate --run-syncdb

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Checking current migrations..."
python manage.py showmigrations

echo "Running database migrations..."
python manage.py migrate --verbosity=2

echo "Creating superuser if needed..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo "Verifying database tables..."
python manage.py shell -c "from django.db import connection; print('Tables:', connection.introspection.table_names())"

echo "Build completed successfully!"
