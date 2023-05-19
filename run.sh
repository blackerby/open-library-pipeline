#!/usr/bin/env bash

PREFECT_API_KEY=$1
PREFECT_WORKSPACE=$2
PREFECT_API_URL=$3

prefect cloud login -k $PREFECT_API_KEY -w $PREFECT_WORKSPACE
prefect config set PREFECT_API_URL=$PREFECT_API_URL

python web_to_gcs_deployment.py
python gcs_to_dataproc_deployment.py

prefect agent start -q 'default'
