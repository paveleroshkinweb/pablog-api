SHELL := /bin/bash

.PHONY: all start-cluster stop-cluster logs connect stop unit-test integration-test pyshell dbshell redishell migrations drop-migrations migrate check-migrations check-server-cfg schema lint lint-fix mypy bandit init-dev-structure check-docker check-nginx clean

all:
	# intentionally left empty to prevent accidental run of first recipe


# -------------------------------------------------
# DEVELOPMENT
# -------------------------------------------------
start-cluster:
	./bin/cluster/local_cluster_control.sh start-cluster

stop-cluster:
	./bin/cluster/local_cluster_control.sh stop-cluster

logs:
	./bin/cluster/local_cluster_control.sh logs

pyshell:
	./bin/cluster/local_cluster_control.sh pyshell

dbshell:
	./bin/cluster/local_cluster_control.sh dbshell

redishell:
	./bin/cluster/local_cluster_control.sh redishell

connect:
	./bin/cluster/local_cluster_control.sh connect $(service)

stop:
	./bin/cluster/local_cluster_control.sh stop $(service)

migrations:
	./bin/cluster/local_cluster_control.sh migrations $(name)

drop-migrations:
	./bin/cluster/local_cluster_control.sh drop-migrations

migrate:
	./bin/cluster/local_cluster_control.sh migrate $(rev)

check-migrations:
	./bin/cluster/local_cluster_control.sh check-migrations


# -------------------------------------------------
# TESTS
# -------------------------------------------------
unit-test:
	./bin/testing_utils/run_tests.sh unit

integration-test:
	./bin/testing_utils/run_tests.sh integration


# -------------------------------------------------
# CI
# -------------------------------------------------
check-server-cfg:
	set -a \
		&& source .env.example \
		&& poetry run gunicorn --config pablog_api/gunicorn_conf.py --check-config pablog_api.api:app

schema:
	set -a \
		&& source .env.example \
		&& poetry run python pablog_api/main.py schema

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
	mkdir -p logs/cache
	touch logs/pablog.logs

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	rm -fr logs/*
	rm -fr pid/*
	docker-compose -f ./compose/docker-compose.server.yaml rm
