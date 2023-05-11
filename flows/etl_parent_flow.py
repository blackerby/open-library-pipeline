from io import BytesIO

import requests
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_gcp.cloud_storage import GcsBucket

gcs_bucket = GcsBucket.load("open-library-raw")


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> BytesIO:
    """Read data from web into BytesIO object"""
    response = requests.get(dataset_url, stream=True)
    buf = BytesIO()
    buf.write(response.content)
    buf.seek(0)
    return buf


@task(retries=3)
def write_to_gcs(data: BytesIO, path: str) -> None:
    """Write file-like object to GCS"""
    gcs_bucket.upload_from_file_object(data, path)


@flow()
def etl_web_to_gcs(dump_type: str):
    """The main ETL flow"""
    dataset_filename = f"ol_dump_{dump_type}_latest.txt.gz"
    dataset_url = f"https://openlibrary.org/data/{dataset_filename}"

    data = fetch(dataset_url)
    write_to_gcs(data, dataset_filename)


@flow(log_prints=True)
def etl_parent_flow(
    dump_types: list[str] = ["authors", "works", "ratings", "reading-log"]
):
    for dt in dump_types:
        etl_web_to_gcs(dt)


if __name__ == "__main__":
    etl_parent_flow()
