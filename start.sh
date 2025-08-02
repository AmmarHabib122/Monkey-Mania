#!/bin/bash

# set production port
if [[ -z "${PRODUCTION}" ]]; then
  WEB_PORT=8000
  PRODUCTION='True'
fi

# Collect static files
echo "Collecting static files"
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python3 manage.py migrate

# Start server
if [[ "${PRODUCTION}" = "True" || "${STAGING_TEST}" = "True" ]]
then
  echo "Starting server"
  gunicorn MonkeyMania.wsgi:application --workers=2 --bind=0.0.0.0:8555
else
  echo "Starting development server"
  python3 manage.py runserver 0.0.0.0:"${WEB_PORT}"
fi
