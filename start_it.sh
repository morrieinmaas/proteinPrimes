#!/bin/bash
#
# Author: Moritz Schlichting
# Email: 2718281@potonmail.ch

# Build the django docker
docker build .

# Migrate the database from django models
docker-compose run web python /code/manage.py migrate --noinput

# create a superuser for admin panel
# comment this out if you have created such user already and you do not wish to create another one
docker-compose run web python /code/manage.py createsuperuser

# Spawn Django, Redis and PostgreSQL with docker compose
docker-compose up -d --build

# And run it on localhost:8000
docker-compose run web python manage.py runserver

# And start a celery worker
docker-compose run web celery worker -A proteinPrimes -l info
