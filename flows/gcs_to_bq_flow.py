from io import BytesIO

import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task
def gcs_to_pd(record_type: str) -> pd.DataFrame:
    """Read dump data into DataFrame"""
    gcs_path = f"ol_dump_{record_type}_latest.txt"
    gcs_bucket = GcsBucket.load("open-library-raw")
    data = BytesIO(gcs_bucket.read_path(path=f"{gcs_path}"))
    data.seek(0)

    if record_type == "ratings":
        names = ["work", "edition", "rating", "date"]
    else:
        names = ["work", "edition", "shelf", "date"]

    return pd.read_csv(data, sep="\t", names=names)


@task
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Date column from string to datetime"""
    df["date"] = pd.to_datetime(df["date"])
    return df


@task
def write_bq(df: pd.DataFrame, record_type: str):
    """Write DataFrame to BigQuery"""
    gcp_creds = GcpCredentials.load("open-library-pipelines-gcp-credentials")

    df.to_gbq(
        destination_table=f"open_library.{record_type}",
        project_id="open-library-pipeline",
        credentials=gcp_creds.get_credentials_from_service_account(),
        chunksize=1_000_000,
        if_exists="replace",
    )


@flow(log_prints=True)
def etl_gcs_to_bq(record_types=["ratings", "reading-log"]):
    """Main ETL flow to load data into Big Query"""
    for rt in record_types:
        df = gcs_to_pd(rt)
        df = transform(df)
        write_bq(df, rt)


if __name__ == "__main__":
    etl_gcs_to_bq()
