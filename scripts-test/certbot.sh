#!/bin/bash

/usr/bin/certbot renew --webroot --webroot-path /usr/data/certbot --http-01-port=8080
if [ $(find /etc/letsencrypt/live/test.theconf.ru -mtime -1 -type l -name "cert.pem" 2>/dev/null) ]
    then
    /usr/bin/docker exec -ti app_nginx service nginx reload
else
    echo "skipped"
fi