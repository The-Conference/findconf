#!/bin/bash

sleep 20

source /app/Conferences/.env
export DJANGO_SUPERUSER_PASSWORD=$(echo $DJANGO_PASS)
export DJANGO_SUPERUSER_EMAIL="admin@email.no"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username $(echo $DJANGO_USER) --no-input
#python manage.py createcachetable
#python manage.py collectstatic  --noinput
gunicorn Conferences.wsgi:application --bind 0.0.0.0:8000

exec "$@"