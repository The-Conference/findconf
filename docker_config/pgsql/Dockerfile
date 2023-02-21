FROM postgres:latest
ADD ./pg_hba.conf /var/lib/postgresql/data/
COPY ./init.sql /docker-entrypoint-initdb.d/