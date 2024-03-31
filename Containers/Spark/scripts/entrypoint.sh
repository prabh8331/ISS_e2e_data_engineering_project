#!/bin/bash
set -e

export PIP_NO_CACHE_DIR=1

if [ -e "/opt/bitnami/spark/requirements.txt" ]; then
  $(command python) pip install --upgrade pip
  $(command -v pip) install -r /opt/bitnami/spark/requirements.txt
fi

exec "$@"

# When you run docker-compose up, the command you specify after the service name (spark-master or spark-worker) will be passed as arguments to the entrypoint script