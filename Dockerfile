FROM prefecthq/prefect:2-python3.10

COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

ARG PREFECT_API_KEY
ENV PREFECT_API_KEY=$PREFECT_API_KEY
ARG PREFECT_API_URL
ENV PREFECT_API_URL=$PREFECT_API_URL
ARG PREFECT_WORKSPACE
ENV PREFECT_WORKSPACE=$PREFECT_WORKSPACE
ENV PYTHONUNBUFFERED True
ENV EXTRA_PIP_PACKAGES gcsfs

COPY flows/ /opt/prefect/flows/

CMD prefect cloud login -k $PREFECT_API_KEY -w $PREFECT_WORKSPACE
CMD prefect config set PREFECT_API_URL=$PREFECT_API_URL
ENTRYPOINT prefect agent start -q default
