#!/bin/bash

set -o errexit  
set -o pipefail  
set -o nounset

function exists_in_list() {
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    LIST_WHITESPACES=`echo $LIST | tr "$DELIMITER" " "`
    for x in $LIST_WHITESPACES; do
        if [ "$x" = "$VALUE" ]; then
            return 0
        fi
    done
    return 1
}

PROCESS_TYPE=$1


if [ "$PROCESS_TYPE" = "server" ]; then
  gunicorn --config pablog_api/gunicorn_conf.py pablog_api.api.server:app
else
  exec "$@"
fi
