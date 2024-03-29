SHELL := /bin/bash

.PHONY: all prod-server unit-test shell check-server-cfg schema lint fix mypy bandit init-dev-structure check-docker check-nginx clean

all:
	# intentionally left empty to prevent accidental run of first recipe

prod-server:
	docker-compose --env-file .env -f ./compose/docker-compose.server.yaml up --build

unit-test:
	set -a && source tests/unit/.env.test && poetry run pytest tests/unit

shell:
	set -a && source .env && poetry run ipython

check-server-cfg:
	set -a && source .env.example && poetry run gunicorn --config pablog_api/gunicorn_conf.py --check-config pablog_api.api.server:app

schema:
	 poetry run python pablog_api/main.py schema

lint:
	poetry run ruff check .

fix:
	poetry run ruff check --fix .

mypy:
	poetry run mypy

bandit:
	poetry run bandit -r pablog_api/

init-dev-structure:
	mkdir -p pid
	mkdir -p logs
	touch logs/pablog.logs

check-docker:
	docker run --rm -i hadolint/hadolint hadolint --ignore DL3008 --ignore DL4006 - < Dockerfile

check-nginx:
	docker run --rm -v ./nginx/nginx.conf:/etc/nginx/nginx.conf -v ./nginx/site.conf:/etc/nginx/conf.d/default.conf -v ./nginx/api_json_errors.conf:/etc/nginx/api_json_errors.conf -v ./nginx/extra_headers.conf:/etc/nginx/extra_headers.conf -v ./nginx/disable_logs.conf:/etc/nginx/disable_logs.conf nginx nginx -t

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	rm -fr logs/*
	rm -fr pid/*
