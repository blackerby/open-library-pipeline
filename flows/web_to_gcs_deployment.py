from etl_parent_flow import etl_parent_flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect_gcp.cloud_storage import GcsBucket

deployment = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="ETL Parent Flow",
    schedule=(CronSchedule(cron="0 0 5 * *")),
    storage=GcsBucket.load("open-library-pipeline-gcs-storage"),
)

if __name__ == "__main__":
    deployment.apply()
