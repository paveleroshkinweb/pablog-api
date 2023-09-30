SHELL := /bin/bash
 
# .PHONY: all devenv devenv-down migrations migrate run-tests testenv testenv-down

all:
	# intentionally left empty to prevent accidental run of first recipe

lint:
	poetry run ruff check .

fix:
	poetry run ruff check --fix .

mypy:
	poetry run mypy

bandit:
	poetry run bandit pablog_api

clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
