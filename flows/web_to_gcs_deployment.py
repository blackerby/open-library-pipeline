from web_to_gcs_flow import etl_parent_flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.filesystems import GCS

deployment = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="Web to GCS Flow",
    schedule=(CronSchedule(cron="0 0 5 * *")),
    storage=GCS.load("open-library-pipeline-gcs-storage"),
)

if __name__ == "__main__":
    deployment.apply()
