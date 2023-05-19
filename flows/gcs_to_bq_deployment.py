from gcs_to_bq_flow import etl_gcs_to_bq
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.filesystems import GCS

deployment = Deployment.build_from_flow(
    flow=etl_gcs_to_bq,
    name="GCS to BigQuery Flow",
    schedule=(CronSchedule(cron="20 0 5 * *")),
    storage=GCS.load("open-library-pipeline-gcs-storage"),
)

if __name__ == "__main__":
    deployment.apply()
