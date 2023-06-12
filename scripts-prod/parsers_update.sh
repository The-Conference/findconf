#!/bin/bash

temp_dir="/tmp/download"
now=$(date +'%Y-%m-%dT%H-%M-%S')

if [ ! -d $temp_dir ]; then
    mkdir $temp_dir
fi

cp -R /usr/data/scrapy /usr/data/scrapy_app-$now-man

cd $temp_dir && wget https://github.com/The-Conference/findconf/archive/refs/heads/scrapy-standalone.zip
unzip $temp_dir/scrapy-standalone.zip
cd /usr/data && docker-compose down
docker rmi $(docker images -q data-scrapy:latest)
rm -rf /usr/data/scrapy/*
cp -R $temp_dir/scrapy-standalone/* /usr/data/scrapy
rm -rf /usr/data/scrapy/.gitignore /usr/data/scrapy/docker-compose.yml /usr/data/scrapy/README.md
cp -rf /root/scrapy/settings.py /usr/data/scrapy/conf_parsers/
rm -rf $temp_dir/scrapy-standalone.zip $temp_dir/scrapy-standalone

cd /usr/data && docker-compose up -d
