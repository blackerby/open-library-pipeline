FROM prefecthq/prefect:2-python3.10

ARG PREFECT_API_KEY
ENV PREFECT_API_KEY=$PREFECT_API_KEY
ARG PREFECT_API_URL
ENV PREFECT_API_URL=$PREFECT_API_URL
ARG PREFECT_WORKSPACE
ENV PREFECT_WORKSPACE=$PREFECT_WORKSPACE
ARG CLUSTER_NAME
ENV CLUSTER_NAME=$CLUSTER_NAME
ARG REGION
ENV REGION=$REGION

COPY docker-requirements.txt .
RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows/ /opt/prefect/flows/
COPY batch/ /opt/prefect/flows/batch/
WORKDIR /opt/prefect/flows

COPY run.sh .
RUN chmod +x run.sh

ENTRYPOINT ./run.sh \
    $PREFECT_API_KEY \
    $PREFECT_WORKSPACE \
    $PREFECT_API_URL
