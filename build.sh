#!/usr/bin/env bash

docker build \
    --build-arg "PREFECT_API_KEY=$PREFECT_API_KEY" \
    --build-arg "PREFECT_API_URL=$PREFECT_API_URL" \
    --build-arg "PREFECT_WORKSPACE=$PREFECT_WORKSPACE" \
    --build-arg "CLUSTER_NAME=$CLUSTER_NAME" \
    --build-arg "REGION=$REGION" \
    -t blackerby/open_library_pipeline \
    .
