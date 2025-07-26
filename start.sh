#!/usr/bin/env bash
set -o errexit

echo "Starting Django application..."

# Check if database exists and is migrated
echo "Checking database status..."
python manage.py showmigrations --plan

# Run any pending migrations
echo "Running any pending migrations..."
python manage.py migrate --verbosity=1

# Start the server
echo "Starting server..."
exec daphne -b 0.0.0.0 -p ${PORT:-8000} mytodo.asgi:application
