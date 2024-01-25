# Utilisez une image de base Python 3
FROM python:3

# Définir un répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source de l'application dans le conteneur
COPY ./app/ /app/

RUN chmod +x /app/run_server.sh

EXPOSE 8000

# Exécuter l'application
ENTRYPOINT ["./run_server.sh"]