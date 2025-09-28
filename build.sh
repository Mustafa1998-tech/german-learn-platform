#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements_prod.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
