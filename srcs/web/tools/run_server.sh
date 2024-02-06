#!/bin/sh

sleep 5

python /app/django/manage.py makemigrations
python /app/django/manage.py migrate

# Ajouter les utilisateurs par défaut
python /app/django/manage.py add_default_users

python /app/django/manage.py collectstatic --noinput

python /app/django/manage.py runserver 0.0.0.0:8000
