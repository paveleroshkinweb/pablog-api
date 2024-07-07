#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


TEST_TYPE=$1

if [ "$TEST_TYPE" = "unit" ]; then
  poetry run pytest tests/unit
elif [ "$TEST_TYPE" = "integration" ]; then
  poetry run pytest tests/integration
fi
