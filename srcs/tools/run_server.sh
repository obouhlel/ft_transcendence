#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Ajouter les utilisateurs par défaut
python manage.py add_default_data

python manage.py collectstatic --noinput

python manage.py watch_file &
python manage.py runserver 0.0.0.0:8000

python manage.py watch_file &
