#!/bin/bash

# this file is for migrating postgresql

if [ "$DATABASE" = "postgres" ]; then
    echo "Check if database is running..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done 

    echo "db is up and running"
fi
python manage.py makemigrations
python manage.py migrate

exec "$@"