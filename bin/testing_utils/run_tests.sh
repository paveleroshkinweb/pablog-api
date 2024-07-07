#!/bin/bash

set -o errexit
set -o pipefail

COMMAND=$1

if [ -z "$PYTHON_VERSION" ]; then
  BUILD_PYTHON_VERSION="3.11-slim"
else
  BUILD_PYTHON_VERSION="${PYTHON_VERSION}"
fi


if [ "$COMMAND" = "unit" ]; then
    docker build --build-arg="PYTHON_VERSION=$BUILD_PYTHON_VERSION" --target test -t pablog-test .
    docker run --env-file tests/unit/.env.test pablog-test unit
elif [ "$COMMAND" = "integration" ]; then
    docker-compose -f ./compose/docker-compose.test.yaml stop
    docker-compose -f ./compose/docker-compose.test.yaml run --build --service-ports test integration
fi
