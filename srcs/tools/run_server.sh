#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Ajouter les utilisateurs par défaut
python manage.py add_default_data


if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

# Enlever le watch_file à la fin du projet srcs/app/transcendence/management/commands/watch_file.py

# python manage.py watch_file &
