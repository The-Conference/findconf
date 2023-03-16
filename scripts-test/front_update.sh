#!/bin/bash

cd /tmp/distrib && wget https://github.com/The-Conference/findconf/archive/refs/heads/frontend.zip
unzip /tmp/distrib/frontend.zip
rm -rf /usr/data/www/*
cp -R /tmp/distrib/findconf-frontend/build/* /usr/data/www
rm -rf /tmp/distrib/findconf-frontend /tmp/distrib/frontend.zip
