#!/bin/sh

# Créer le répertoire pour le certificat SSL
mkdir -p /etc/nginx/ssl

# Générer un certificat SSL auto-signé
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/transcendance.key \
    -out /etc/nginx/ssl/transcendance.crt \
    -subj "/C=FR/ST=Paris/L=Paris/O=Global Security/OU=IT Department/CN=transcendance.local"

# Démarrer NGINX
nginx -g "daemon off;"