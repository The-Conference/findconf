#!/bin/bash

temp_dir="/tmp/download"
now=$(date +'%Y-%m-%dT%H-%M-%S')

if [ ! -d $temp_dir ]; then
    mkdir $temp_dir
fi

cp -R /usr/data/django/app /usr/data/django_app-$now-man

cd $temp_dir && wget https://github.com/The-Conference/findconf/archive/refs/heads/backend.zip
unzip $temp_dir/backend.zip
cd /usr/data && docker-compose down
docker rmi $(docker images -q data-django:latest)
docker rmi $(docker images -q data-celery:latest)
rm -rf /usr/data/django/app/*
cp -R $temp_dir/findconf-backend/* /usr/data/django/app
cp -rf /root/.env /usr/data/django/app/Conferences/
cp -rf /root/settings.py /usr/data/django/app/Conferences/
rm -rf $temp_dir/findconf-backend $temp_dir/backend.zip

cd /usr/data && docker-compose up -d
