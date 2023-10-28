SHELL := /bin/bash

.PHONY: all server check-server-cfg lint fix mypy bandit clean

all:
	# intentionally left empty to prevent accidental run of first recipe

server:
	gunicorn --config pablog_api/gunicorn.conf.py pablog_api.api.server:app

check-server-cfg:
	gunicorn --config pablog_api/gunicorn.conf.py --check-config pablog_api.api.server:app

lint:
	poetry run ruff check .

fix:
	poetry run ruff check --fix .

mypy:
	poetry run mypy

bandit:
	poetry run bandit pablog_api -r

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
