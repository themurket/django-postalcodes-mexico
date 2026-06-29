#!/bin/bash
set -e

echo "Applying database migrations"
python manage.py migrate --noinput
python manage.py importpostalcodesmx

echo "Starting Django dev server with autoreload"
exec python manage.py runserver 0.0.0.0:8000
