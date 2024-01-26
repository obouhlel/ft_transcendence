#!/bin/sh

python /app/django/manage.py makemigrations
python /app/django/manage.py migrate

python /app/django/manage.py collectstatic --noinput

python /app/django/manage.py runserver 0.0.0.0:8000