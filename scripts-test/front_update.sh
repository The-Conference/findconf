#!/bin/bash

temp_dir="/tmp/download"

if [ ! -d $temp_dir ]; then
    mkdir $temp_dir
fi

cd $temp_dir && wget https://github.com/The-Conference/findconf/archive/refs/heads/frontend.zip
unzip $temp_dir/frontend.zip
rm -rf /usr/data/www/*
cp -R $temp_dir/findconf-frontend/build/* /usr/data/www
rm -rf $temp_dir/findconf-frontend $temp_dir/frontend.zip