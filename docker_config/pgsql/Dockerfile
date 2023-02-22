FROM postgres:latest
RUN rm -f /var/lib/postgresql/data/pg_hba.conf
ADD ./pg_hba.conf /var/lib/postgresql/data/
COPY ./init.sql /docker-entrypoint-initdb.d/