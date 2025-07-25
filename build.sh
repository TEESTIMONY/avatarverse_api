#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Create media directory if it doesn't exist
mkdir -p media/avatars

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate 