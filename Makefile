DOCKER=web

all: clean up logs

reset: clean down build up logs

exec:
	docker exec -it $(DOCKER) sh

ps:
	docker compose ps

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

stop:
	docker compose stop

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	rm -rf srcs/app/transcendence/migrations/0*.py

fclean: clean stop
	docker system prune -a -f --volumes
	if [ "$$(docker volume ls -q)" != "" ]; then \
		docker volume rm $$(docker volume ls -q); \
	fi

re: fclean all

.PHONY: all build up down logs re build