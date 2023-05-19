import os

from prefect import task, flow
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket
from google.cloud import dataproc_v1

gcp_credentials_block = GcpCredentials.load("open-library-pipelines-gcp-credentials")
gcs_jobs_bucket = GcsBucket.load("olp-dataproc-jobs")


@task
def write_job_to_gcs(dump_type: str):
    """Write file-like object to GCS"""
    path = f"batch/{dump_type}.py"
    print(f"uploading {path}")
    gcs_jobs_bucket.upload_from_path(path, path)


@task
def gcs_to_dataproc(record_type: str):
    cluster_name = os.environ["CLUSTER_NAME"]
    region = os.environ["REGION"]
    api = f"{region}-dataproc.googleapis.com:443"
    credentials = gcp_credentials_block.get_credentials_from_service_account()

    client = dataproc_v1.JobControllerClient(
        credentials=credentials, client_options={"api_endpoint": api}
    )
    job = dataproc_v1.Job()
    job.pyspark_job.main_python_file_uri = (
        f"gs://{gcs_jobs_bucket.bucket}/batch/{record_type}.py"
    )
    job.pyspark_job.jar_file_uris = [
        "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
    ]
    job.placement.cluster_name = cluster_name
    request = dataproc_v1.SubmitJobRequest(
        project_id="open-library-pipeline", region=region, job=job
    )
    operation = client.submit_job_as_operation(
        request=request,
    )
    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)


@flow(log_prints=True)
def gcs_to_dataproc_parent_flow(dump_types: list[str] = ["authors", "works"]):
    for dt in dump_types:
        write_job_to_gcs(dt)
        print(f"Transforming {dt} with Dataproc")
        gcs_to_dataproc(dt)


if __name__ == "__main__":
    gcs_to_dataproc_parent_flow()
