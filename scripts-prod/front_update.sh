#!/bin/bash

temp_dir="/tmp/download"
now=$(date +'%Y-%m-%dT%H-%M-%S')

if [ ! -d $temp_dir ]; then
    mkdir $temp_dir
fi

cp -R /usr/data/www /usr/data/www-$now-man

cd $temp_dir && wget https://github.com/The-Conference/findconf/archive/refs/heads/frontend-for-prod.zip
unzip $temp_dir/frontend-for-prod.zip
rm -rf /usr/data/www/*
cp -R $temp_dir/findconf-frontend-for-prod/build/* /usr/data/www
rm -rf $temp_dir/findconf-frontend-for-prod $temp_dir/frontend-for-prod.zip
