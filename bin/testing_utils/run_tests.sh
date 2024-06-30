#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

COMMAND=$1

if [ "$COMMAND" = "unit-test" ]; then
    docker build --target test -t pablog-test .
    docker run --env-file tests/unit/.env.test pablog-test
fi
