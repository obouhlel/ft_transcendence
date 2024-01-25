#!/bin/bash

# Exécute les migrations
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

# Exécute la commande CMD du Dockerfile
python manage.py runserver 0.0.0.0:8000
# python manage.py runserver