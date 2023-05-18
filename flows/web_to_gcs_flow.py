from pathlib import Path
import gzip
import os
import shutil

import requests
from prefect import task, flow
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_gcp.cloud_storage import GcsBucket

BASE_URL = "https://openlibrary.org/data/"

gcs_bucket = GcsBucket.load("open-library-raw")
gcp_credentials_block = GcpCredentials.load("open-library-pipelines-gcp-credentials")
gcs_jobs_bucket = GcsBucket.load("olp-dataproc-jobs")


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_filename: str):
    """Read data from web and write to file on disk"""
    dataset_url = f"{BASE_URL}{dataset_filename}"
    print(f"fetching {dataset_url}")
    response = requests.get(dataset_url)
    with open(dataset_filename, "wb") as f:
        print(f"writing {dataset_filename}")
        f.write(response.content)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def gunzip(filename: str):
    print(f"decompressing {filename}")
    outfile = Path(filename).stem
    print(f"writing {outfile}")
    with gzip.open(filename, "r") as f_in, open(outfile, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"removing {filename}")
    os.remove(filename)


@task
def write_to_gcs(path: str):
    """Write file-like object to GCS"""
    print(f"uploading {path}")
    gcs_bucket.upload_from_path(path, path)
    print(f"removing {path}")
    os.remove(path)


@flow
def etl_web_to_gcs(dump_type: str):
    """The main ETL flow"""
    dataset_filename = f"ol_dump_{dump_type}_latest.txt.gz"

    fetch(dataset_filename)
    gunzip(dataset_filename)
    write_to_gcs(Path(dataset_filename).stem)


@flow(log_prints=True)
def etl_parent_flow(
    dump_types: list[str] = ["ratings", "reading-log", "authors", "works"]
):
    for dt in dump_types:
        print(f"Uploading {dt} to GCS")
        etl_web_to_gcs(dt)


if __name__ == "__main__":
    etl_parent_flow()
