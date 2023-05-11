FROM prefecthq/prefect:2-python3.10

ARG PREFECT_API_KEY
ENV PREFECT_API_KEY=$PREFECT_API_KEY
ARG PREFECT_API_URL
ENV PREFECT_API_URL=$PREFECT_API_URL
ARG PREFECT_WORKSPACE
ENV PREFECT_WORKSPACE=$PREFECT_WORKSPACE
ARG SCRIPT_NAME
ENV SCRIPT_NAME=$SCRIPT_NAME
ARG FLOW_TAG
ENV FLOW_TAG=$FLOW_TAG
ARG DEPLOYMENT_NAME
ENV DEPLOYMENT_NAME=$DEPLOYMENT_NAME
ARG CRON
ENV CRON=$CRON

COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows/ /opt/prefect/flows/
WORKDIR /opt/prefect/flows

COPY run.sh .
RUN chmod +x run.sh

ENTRYPOINT ./run.sh \
    $PREFECT_API_KEY \
    $PREFECT_WORKSPACE \
    $PREFECT_API_URL \
    $SCRIPT_NAME \
    $FLOW_TAG \
    $DEPLOYMENT_NAME \
    $CRON
