#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --clear

# Run database migrations
python manage.py migrate

# Create superuser (if not exists)
python manage.py createsuperuser --noinput || true