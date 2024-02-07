FROM alpine:latest

LABEL key='[Django]'

RUN apk update && apk add --no-cache \
	python3 \
	py3-pip \
	openssl

RUN mkdir -p /app /var/www

WORKDIR /app

RUN mkdir -p /app/django

RUN python3 -m venv venv
RUN source venv/bin/activate

ENV PATH="/app/venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=django_app.settings

COPY ./tools/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN openssl req -x509 -out /etc/ssl/certs/localhost.crt -keyout /etc/ssl/private/localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")

COPY ./tools/run_server.sh /app

RUN chmod +x /app/run_server.sh

EXPOSE 8000

WORKDIR /app/django

ENTRYPOINT ["sh", "/app/run_server.sh"]
# for debug
# CMD ["sh", "-c", "while true; do sleep inf; done"]
