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
    docker-compose --env-file tests/integration/.env.test -f compose/docker-compose.test.yaml up --abort-on-container-exit --build
fi
