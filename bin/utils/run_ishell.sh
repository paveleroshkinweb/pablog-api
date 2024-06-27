#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


if [ "$( docker container inspect -f '{{.State.Running}}' pablog-api )" != "true" ]; then
  nohup make prod-server &
fi


while [ "$( docker container inspect -f '{{.State.Running}}' pablog-api )" != "true" ]
do
  echo "Waiting till local cluster is up and running"
  sleep 4
done


set -a \
		&& source ./compose/server/.env.server \
		&& export postgres_db_host=127.0.0.1 \
		&& poetry run ipython
