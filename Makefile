SHELL := /bin/bash

.PHONY: all server unit-test py-shell c-bash migrations migrate check-server-cfg schema lint lint-fix mypy bandit init-dev-structure check-docker check-nginx clean

all:
	# intentionally left empty to prevent accidental run of first recipe


# -------------------------------------------------
# DEVELOPMENT
# -------------------------------------------------
server:
	docker-compose --env-file ./compose/db/.env.db -f ./compose/docker-compose.server.yaml up --build

py-shell:
	./bin/utils/run_ishell.sh

c-bash:
	docker exec -u root -it pablog-api /bin/bash

migrations:
	./bin/utils/run_migrations.sh

migrate:
	./bin/utils/migrate.sh

# -------------------------------------------------
# TESTS
# -------------------------------------------------
unit-test:
	set -a && source tests/unit/.env.test && poetry run pytest tests/unit


# -------------------------------------------------
# CI
# -------------------------------------------------
check-server-cfg:
	set -a \
		&& source .env.example \
		&& poetry run gunicorn --config pablog_api/gunicorn_conf.py --check-config pablog_api.api.server:app

schema:
	 poetry run python pablog_api/main.py schema

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check --fix .

mypy:
	poetry run mypy

bandit:
	poetry run bandit -r pablog_api/

check-docker:
	docker run --rm -i hadolint/hadolint hadolint --ignore DL3008 --ignore DL4006 - < Dockerfile

check-nginx:
	docker run --rm -v ./compose/nginx/nginx.conf:/etc/nginx/nginx.conf \
					-v ./compose/nginx/site.conf:/etc/nginx/conf.d/default.conf \
					-v ./compose/nginx/api_json_errors.conf:/etc/nginx/api_json_errors.conf \
					-v ./compose/nginx/extra_headers.conf:/etc/nginx/extra_headers.conf \
					-v ./compose/nginx/disable_logs.conf:/etc/nginx/disable_logs.conf \
					nginx nginx -t


# -------------------------------------------------
# UTILS
# -------------------------------------------------
init-dev-structure:
	chmod -R +x bin
	mkdir -p pid
	mkdir -p logs
	mkdir -p logs/postgresql
	touch logs/pablog.logs

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	rm -fr logs/*
	rm -fr pid/*
	docker rm pablog-masterdb
	docker rm nginx-frontend
	docker rm pablog-api
