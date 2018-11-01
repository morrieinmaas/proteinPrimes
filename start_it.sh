#!/bin/bash
#
# Author: Moritz Schlichting
# Email: 2718281@potonmail.ch

# Build the django docker
docker build .

# Migrate the database from django models
docker-compose run web python /code/manage.py migrate --noinput

# create a superuser for admin panel
docker-compose run web python /code/manage.py createsuperuser

# Spawn Django, Redis and PostgreSQL with docker compose
docker-compose up -d --build
