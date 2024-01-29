FROM alpine:3.17

RUN addgroup -g 101 -S nginx
RUN adduser -S -D -H -u 101 -h /var/cache/nginx \
    -s /sbin/nologin -G nginx -g nginx nginx

RUN apk update && apk upgrade
RUN apk add nginx curl openssl --no-cache

RUN mkdir -p /var/run/nginx /etc/nginx/ssl /var/www/static

RUN openssl req -x509 -nodes -out /etc/nginx/ssl/transcendance.crt \
    -keyout /etc/nginx/ssl/transcendance.key -subj \
    "/C=FR/ST=IDF/L=Paris/O=42/OU=42/CN=transcendance.42.fr/UID=transcendance"

COPY ./conf/nginx.conf /etc/nginx/nginx.conf

RUN chown -R nginx:nginx /var/www/static \
  && chown -R nginx:nginx /var/lib/nginx \
  && chown -R nginx:nginx /etc/nginx \
  && chmod 755 /var/www/static

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 8080

USER nginx

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]