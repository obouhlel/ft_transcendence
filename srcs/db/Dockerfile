FROM alpine:latest

LABEL key='[PostgreSQL]'

RUN apk update && apk add --no-cache \
	postgresql \
	postgresql-client \
	postgresql-contrib \
	vim

RUN mkdir -p /app /var/www

WORKDIR /app

COPY ./tools/init_db.sh /app

RUN chmod +x /app/init_db.sh

EXPOSE 5432

ENTRYPOINT ["sh", "/app/init_db.sh"]