#!/bin/bash
set -e

echo "Applying database migrations"
python manage.py migrate --noinput
python manage.py importpostalcodesmx

echo "Starting Gunicorn"
exec gunicorn codigosPostalesMx.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
