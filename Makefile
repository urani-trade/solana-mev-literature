.PHONY: setup install clean test lint populate populate_imp staging prod awsstatic

default: run

install:
	pipenv install

run:
	python manage.py runserver

clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@find . -type d -name '*.ropeproject' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg*
	@rm -f MANIFEST

populate:
	python manage.py populate data/data.json

populate_imp:
	python manage.py populate_imp data/cleaned_data.json

awsstatic:
	python manage.py collectstatic

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

test:
	python manage.py test

staging:
	now

prod:
	now --prod

lint:
	@tox -e flake8
