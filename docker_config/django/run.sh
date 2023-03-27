#!/bin/bash

sleep 20

source /app/Conferences/.env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py createcachetable
python manage.py collectstatic  --noinput
gunicorn --certfile=/etc/letsencrypt/live/test.theconf.ru/cert.pem --keyfile=/etc/letsencrypt/live/test.theconf.ru/privkey.pem Conferences.wsgi:application --bind 0.0.0.0:8000

exec "$@"

