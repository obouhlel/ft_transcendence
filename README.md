# Environement file

name : .env

position : ./ (at the root of project)

env file :
```
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
DOMAIN=
IP=1
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
CLIENT_ID=
CLIENT_SECRET=
```
The CLIENT_SECRET need to be secret and don't print it

# The last of project

- Need to remove the DEBUG = True on settings.py
- Need to remove the watchdir

# Remove all pycache command

```
sudo find . -type d -name __pycache__ -exec rm -r {} +
```
