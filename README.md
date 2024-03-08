# Environement file

name : .env

position : ./ (at the root of project)

env file :
```
DOMAIN=bess-f4r1s9
IP=10.14.1.9
POSTGRES_DB=transcendence
POSTGRES_USER=admin
POSTGRES_PASSWORD=toto
CLIENT_ID=u-s4t2ud-b221266d69284108d856829b7bf94bddec68b82af2a4d2eb994ac4df2978deb5
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
