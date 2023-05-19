from gcs_to_dataproc_flow import gcs_to_dataproc_parent_flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.filesystems import GCS

deployment = Deployment.build_from_flow(
    flow=gcs_to_dataproc_parent_flow,
    name="GCS to Dataproc Flow",
    schedule=(CronSchedule(cron="55 0 5 * *")),
    storage=GCS.load("open-library-pipeline-gcs-storage"),
)

if __name__ == "__main__":
    deployment.apply()
