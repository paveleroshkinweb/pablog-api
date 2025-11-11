#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

COMMAND=$1

if [ "$COMMAND" = "start-cluster" ]; then
    TMP_ENV="/tmp/.temp.env"
    {
      rsa_private_key=$(cat ./compose/server/private_jwt.pem | base64 | tr -d '\n')
      rsa_public_key=$(cat ./compose/server/public_jwt.pem | base64 | tr -d '\n')
      echo "oauth_rsa_private_key=$rsa_private_key"
      echo "oauth_rsa_public_key=$rsa_public_key"
    } > "$TMP_ENV"
    sync "$TMP_ENV"
  
    docker-compose --env-file "$TMP_ENV" -f ./compose/docker-compose.server.yaml up --build
    rm -f $TMP_ENV
    exit 0

elif [ "$COMMAND" = "stop-cluster" ]; then
    docker-compose -f ./compose/docker-compose.server.yaml stop
    exit 0

elif [ "$COMMAND" = "dbshell" ]; then
    sqlite3 ./db/pablog.db
    exit 0

elif [ "$COMMAND" = "drop-migrations" ]; then
    export sqlite_url=sqlite+aiosqlite:///./db/pablog.db
    poetry run alembic stamp base && poetry run alembic downgrade base
    exit 0

elif [ "$COMMAND" = "migrations" ]; then
    export sqlite_url=sqlite+aiosqlite:///./db/pablog.db
    MIGRATIONS_COMMENT=$2
    poetry run alembic revision --autogenerate -m "$MIGRATIONS_COMMENT"
    exit 0

elif [ "$COMMAND" = "migrate" ]; then
    export sqlite_url=sqlite+aiosqlite:///./db/pablog.db
    if [ "$#" -ne 2 ]; then
      poetry run alembic upgrade head
    else
      REVISION=$2
      poetry run alembic upgrade $REVISION
    fi
    exit 0

elif [ "$COMMAND" = "check-migrations" ]; then
    export sqlite_url=sqlite+aiosqlite:///./db/pablog.db
    poetry run alembic check
    exit 0

elif [ "$COMMAND" = "rollback" ]; then
    export sqlite_url=sqlite+aiosqlite:///./db/pablog.db
    poetry run alembic downgrade -1
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


if [ "$COMMAND" = "logs" ]; then
    docker-compose -f ./compose/docker-compose.server.yaml logs --follow

elif [ "$COMMAND" = "connect" ]; then
  SERVICE_NAME=$2
  docker-compose -f ./compose/docker-compose.server.yaml exec -u root -it $SERVICE_NAME /bin/bash

elif [ "$COMMAND" = "stop" ]; then
  SERVICE_NAME=$2
  docker-compose -f ./compose/docker-compose.server.yaml stop $SERVICE_NAME

elif [ "$COMMAND" = "pyshell" ]; then
    docker exec -it pablog-api ipython -i /opt/pablog-service/ipython_helper.py

elif [ "$COMMAND" = "redishell" ]; then
    docker exec -it pablog-cache redis-cli

fi
