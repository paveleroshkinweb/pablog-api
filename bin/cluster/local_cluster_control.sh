#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

COMMAND=$1

if [ "$COMMAND" = "start-cluster" ]; then
    docker-compose --env-file ./compose/db/.env.db -f ./compose/docker-compose.server.yaml up --build
    exit 0
elif [ "$COMMAND" = "stop-cluster" ]; then
    docker stop pablog-masterdb nginx-frontend pablog-api
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

if [ "$COMMAND" = "logs" ]; then
    docker-compose -f ./compose/docker-compose.server.yaml logs --follow
elif [ "$COMMAND" = "py-shell" ]; then
    poetry run ipython
elif [ "$COMMAND" = "c-bash" ]; then
    docker exec -u root -it pablog-api /bin/bash
elif [ "$COMMAND" = "drop-migrations" ]; then
    poetry run alembic stamp base && poetry run alembic downgrade base
elif [ "$COMMAND" = "migrations" ]; then
    MIGRATIONS_COMMENT=$2
    poetry run alembic revision --autogenerate -m "$MIGRATIONS_COMMENT"
elif [ "$COMMAND" = "migrate" ]; then
    poetry run alembic upgrade head
fi
