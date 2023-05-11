#!/usr/bin/env bash

PREFECT_API_KEY=$1
PREFECT_WORKSPACE=$2
PREFECT_API_URL=$3
SCRIPT_NAME=$4
FLOW_TAG=$5
DEPLOYMENT_NAME=$6
INTERVAL=$7

prefect cloud login -k $PREFECT_API_KEY -w $PREFECT_WORKSPACE
prefect config set PREFECT_API_URL=$PREFECT_API_URL
prefect deployment build $SCRIPT_NAME:$FLOW_TAG \
    --name $DEPLOYMENT_NAME \
    --storage-block gcs/open-library-pipeline-gcs-storage \
    --interval $INTERVAL \
    --apply && \
prefect agent start -q 'default'
