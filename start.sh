#!/usr/bin/env bash
set -o errexit

echo "Starting Django application..."

# Ensure database directory exists
mkdir -p /opt/render/project/src

# Check if database exists and is migrated
echo "Checking database status..."
python manage.py showmigrations --plan

# Create database tables from scratch if needed
echo "Creating database tables..."
python manage.py migrate --run-syncdb --verbosity=2

# Run any additional migrations
echo "Running migrations..."
python manage.py migrate --verbosity=2

# Verify tables were created
echo "Verifying database tables..."
python manage.py shell -c "from django.db import connection; tables = connection.introspection.table_names(); print(f'Available tables: {tables}'); print(f'todo_task exists: {\"todo_task\" in tables}')"

# Create superuser if needed
echo "Creating superuser if needed..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" || echo "Superuser creation skipped"

# Start the server
echo "Starting server with tables verification complete..."
exec daphne -b 0.0.0.0 -p ${PORT:-8000} mytodo.asgi:application
