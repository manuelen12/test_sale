#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A test_venta.taskapp beat -l INFO
