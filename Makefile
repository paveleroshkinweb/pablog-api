SHELL := /bin/bash

.PHONY: all server check-server-cfg schema lint fix mypy bandit clean

all:
	# intentionally left empty to prevent accidental run of first recipe

server:
	poetry run gunicorn --config pablog_api/gunicorn.conf.py pablog_api.api.server:app

check-server-cfg:
	poetry run gunicorn --config pablog_api/gunicorn.conf.py --check-config pablog_api.api.server:app

schema:
	 poetry run python pablog_api/main.py schema

lint:
	poetry run ruff check .

fix:
	poetry run ruff check --fix .

mypy:
	poetry run mypy

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
