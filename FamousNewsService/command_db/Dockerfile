FROM postgres

EXPOSE 5435:5432
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d