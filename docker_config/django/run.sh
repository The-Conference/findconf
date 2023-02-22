#!/bin/sh

sleep 15

python manage.py makemigrations
python manage.py migrate
#python manage.py createcachetable
#python manage.py collectstatic  --noinput
gunicorn Conferences.wsgi:application --bind 0.0.0.0:8000

exec "$@"