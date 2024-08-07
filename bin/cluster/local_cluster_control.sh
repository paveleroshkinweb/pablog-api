#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

COMMAND=$1

if [ "$COMMAND" = "start-cluster" ]; then
    docker-compose -f ./compose/docker-compose.server.yaml up --build
    exit 0

elif [ "$COMMAND" = "stop-cluster" ]; then
    docker-compose -f ./compose/docker-compose.server.yaml stop
    exit 0
fi


if [ "$( docker container inspect -f '{{.State.Running}}' pablog-api )" != "true" ]; then
  nohup make start-cluster &
fi


while [ "$( docker container inspect -f '{{.State.Running}}' pablog-api )" != "true" ]
do
  echo "Waiting till local cluster is up and running"
  sleep 4
done

set -a \
		&& source ./compose/server/.env.server \
		&& export postgres_db_host=127.0.0.1 \
		&& export cache_host=127.0.0.1

if [ "$COMMAND" = "logs" ]; then
    docker-compose -f ./compose/docker-compose.server.yaml logs --follow

elif [ "$COMMAND" = "connect" ]; then
  SERVICE_NAME=$2
  docker-compose -f ./compose/docker-compose.server.yaml exec -u root -it $SERVICE_NAME /bin/bash

elif [ "$COMMAND" = "stop" ]; then
  SERVICE_NAME=$2
  docker-compose -f ./compose/docker-compose.server.yaml stop $SERVICE_NAME

elif [ "$COMMAND" = "pyshell" ]; then
    poetry run ipython -i ./bin/utils/ipython_helper.py

elif [ "$COMMAND" = "dbshell" ]; then
    docker exec -it pablog-masterdb psql -U $postgres_db_name

elif [ "$COMMAND" = "redishell" ]; then
    docker exec -it pablog-cache redis-cli

elif [ "$COMMAND" = "drop-migrations" ]; then
    poetry run alembic stamp base && poetry run alembic downgrade base

elif [ "$COMMAND" = "migrations" ]; then
    MIGRATIONS_COMMENT=$2
    poetry run alembic revision --autogenerate -m "$MIGRATIONS_COMMENT"

elif [ "$COMMAND" = "migrate" ]; then
    if [ "$#" -ne 2 ]; then
      poetry run alembic upgrade head
    else
      REVISION=$2
      poetry run alembic upgrade $REVISION
    fi

elif [ "$COMMAND" = "check-migrations" ]; then
    poetry run alembic check

elif [ "$COMMAND" = "rollback" ]; then
    poetry run alembic downgrade -1

elif [ "$COMMAND" = "fetch-config" ]; then
    poetry run python pablog_api/main.py fetch-config

elif [ "$COMMAND" = "write-config" ]; then
    poetry run python pablog_api/main.py write-config
fi
