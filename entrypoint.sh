#!/bin/bash

set -o errexit  
set -o pipefail  
set -o nounset


PROCESS_TYPE=$1


if [ "$PROCESS_TYPE" = "server" ]; then
  gunicorn --config pablog_api/gunicorn_conf.py pablog_api.api.server:app
else
  exec "$@"
fi
