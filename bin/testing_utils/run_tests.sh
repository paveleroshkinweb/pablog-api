#!/bin/bash

set -o errexit
set -o pipefail

COMMAND=$1

if [ -z "$PYTHON_VERSION" ]; then
  BUILD_PYTHON_VERSION="3.11-slim"
else
  BUILD_PYTHON_VERSION="${PYTHON_VERSION}"
fi

docker build --build-arg="PYTHON_VERSION=$BUILD_PYTHON_VERSION" --target test -t pablog-test .

if [ "$COMMAND" = "unit-test" ]; then
    docker run --env-file tests/unit/.env.test pablog-test
fi
