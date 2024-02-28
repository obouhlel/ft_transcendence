# Environement file

name : .env

position : ./ (at the root of project)

env file :
```
POSTGRES_DB=transcendence  
POSTGRES_USER=admin  
POSTGRES_PASSWORD=toto  
CLIENT_ID=u-s4t2ud-5b9c9133859a5333ef620d8fd41e79e5ce3174c4300678ff79c6f12c88a4cf77  
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
