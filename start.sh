#!/usr/bin/env bash
set -o errexit

echo "=== Starting Django application ==="

# Show environment info
echo "Current working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"

# Ensure database directory exists
echo "Creating database directory..."
mkdir -p /opt/render/project/src

# Check current database file
DB_PATH="/opt/render/project/src/db.sqlite3"
echo "Database path: $DB_PATH"
echo "Database file exists: $(test -f $DB_PATH && echo 'Yes' || echo 'No')"
if [ -f "$DB_PATH" ]; then
    echo "Database file size: $(ls -lh $DB_PATH)"
fi

# Check if database exists and is migrated
echo "=== Checking database status ==="
python manage.py showmigrations

# Create fresh migrations if needed (backup approach)
echo "=== Creating fresh migrations ==="
python manage.py makemigrations todo --verbosity=2 || echo "No new migrations needed"

# Create database tables from scratch if needed
echo "=== Creating database tables ==="
python manage.py migrate --run-syncdb --verbosity=2

# Run any additional migrations
echo "=== Running all migrations ==="
python manage.py migrate --verbosity=2

# Force apply specific migrations if they exist
echo "=== Force applying todo migrations ==="
python manage.py migrate todo --verbosity=2 || echo "Todo migrations already applied"

# Verify tables were created
echo "=== Verifying database tables ==="
python manage.py shell -c "
from django.db import connection
import os
from django.conf import settings

tables = connection.introspection.table_names()
print(f'Available tables: {tables}')
print(f'todo_task exists: {\"todo_task\" in tables}')
print(f'Database file: {settings.DATABASES[\"default\"][\"NAME\"]}')
print(f'Database file exists: {os.path.exists(str(settings.DATABASES[\"default\"][\"NAME\"]))}')
if os.path.exists(str(settings.DATABASES['default']['NAME'])):
    print(f'Database file size: {os.path.getsize(str(settings.DATABASES[\"default\"][\"NAME\"]))} bytes')
"

# Create superuser if needed
echo "=== Creating superuser if needed ==="
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" || echo "Superuser creation skipped"

# Start Gunicorn with Uvicorn worker for ASGI
# Use the PORT environment variable provided by Render/Railway, default to 8000
gunicorn mytodo.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

echo "Application started successfully."
