#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py migrate --noinput

/usr/local/bin/gunicorn upwind.wsgi --bind 0.0.0.0:${PORT}