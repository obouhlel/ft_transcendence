all: run

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

clean:
	rm -rf db.sqlite3
	rm -rf */migrations/0*
	rm -rf */migrations/__pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__

re: clean migrate run