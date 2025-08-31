FROM postgres:17

COPY postgres/initdb/init.sql /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/init.sql

EXPOSE 5432