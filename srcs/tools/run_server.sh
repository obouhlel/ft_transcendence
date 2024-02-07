#!/bin/sh

sleep 5

python manage.py makemigrations
python manage.py migrate

# Ajouter les utilisateurs par défaut
# python manage.py add_default_users

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000
# python manage.py runsslserver 0.0.0.0:8000 --certificate /etc/ssl/certs/localhost.crt --key /etc/ssl/private/localhost.key