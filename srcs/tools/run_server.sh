#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Ajouter les utilisateurs par défaut
python manage.py add_default_data

python manage.py collectstatic --noinput

# Enlever le watch_file à la fin du projet srcs/app/transcendence/management/commands/watch_file.py
python manage.py watch_file &
python manage.py runserver 0.0.0.0:8000

python manage.py watch_file &
