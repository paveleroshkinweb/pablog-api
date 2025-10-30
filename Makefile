SHELL := /bin/bash

.PHONY: all start-cluster stop-cluster logs connect stop pyshell dbshell redishell migrations drop-migrations migrate rollback check-migrations schema lint lint-fix mypy init-dev-structure clean

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

rollback:
	./bin/cluster/local_cluster_control.sh rollback

check-migrations:
	./bin/cluster/local_cluster_control.sh check-migrations


# -------------------------------------------------
# CI
# -------------------------------------------------

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

	mkdir -p db
	touch db/pablog.db

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	rm -fr logs/*
	rm -fr pid/*
	docker-compose -f ./compose/docker-compose.server.yaml rm
