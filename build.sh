#!/usr/bin/env bash

SCRIPT_NAME=$1
FLOW_TAG=$2
DEPLOYMENT_NAME=$3
CRON=$4
CLUSTER_NAME=$5
REGION=$6

docker build \
    --build-arg "PREFECT_API_KEY=$PREFECT_API_KEY" \
    --build-arg "PREFECT_API_URL=$PREFECT_API_URL" \
    --build-arg "PREFECT_WORKSPACE=$PREFECT_WORKSPACE" \
    --build-arg "SCRIPT_NAME=$SCRIPT_NAME" \
    --build-arg "FLOW_TAG=$FLOW_TAG" \
    --build-arg "DEPLOYMENT_NAME=$DEPLOYMENT_NAME" \
    --build-arg "CRON=$CRON" \
    --build-arg "CLUSTER_NAME=$CLUSTER_NAME" \
    --build-arg "REGION=$REGION" \
    -t blackerby/open_library_pipeline \
    .
