#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if not exists
# If superuser exists, update password

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
	if [ "$(python manage.py shell -c "from transcendence.models import CustomUser; print(CustomUser.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())")" = "True" ]
	then
		python manage.py shell -c "from transcendence.models import CustomUser; u = CustomUser.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); u.set_password('$DJANGO_SUPERUSER_PASSWORD'); u.save()"
	else
    	python manage.py createsuperuser \
			--noinput \
			--username $DJANGO_SUPERUSER_USERNAME \
			--email $DJANGO_SUPERUSER_EMAIL
	fi
fi

python manage.py add_default_data

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

# Enlever le watch_file à la fin du projet srcs/app/transcendence/management/commands/watch_file.py

# python manage.py watch_file &
