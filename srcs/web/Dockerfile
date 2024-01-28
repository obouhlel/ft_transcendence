FROM alpine:latest

LABEL key='[Django]'

RUN apk update && apk add --no-cache \
	python3 \
	py3-pip

RUN mkdir -p /app /var/www

WORKDIR /app

RUN mkdir -p /app/django

RUN python3 -m venv venv
RUN source venv/bin/activate
ENV PATH="/app/venv/bin:$PATH"

COPY ./tools/requirements.txt .

RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

COPY ./tools/run_server.sh /app

RUN chmod +x /app/run_server.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/app/run_server.sh"]
# for debug
# CMD ["sh", "-c", "while true; do sleep inf; done"]