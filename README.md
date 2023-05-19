# Open Library Pipeline

Workspace for [DataTalksClub's Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Infrastructure

### Cloud Storage

To set up the Google Cloud Storage data lake, Prefect remote storage, and storage for Spark jobs, from the root directory, run

```bash
make apply-storage
```

and follow the prompts.

It is reasonable to leave all the storage up and running, but if for some reason it needs to be removed, run

```bash
make destroy-storage
```

in the root directory.

### Cloud Compute

To set up the Google Compute Engine VM that runs a Docker container for this project and the Google Dataproc Cluster that runs Spark jobs, from the root directory, run

```bash
make apply-compute
```

and follow the prompts.

It is reasonable to take down the VM and the cluster when they are not in use. To do so, run

```bash
make destroy-compute
```

in the root directory.

## Orchestration

The `Dockerfile` builds an image that connects to a Prefect Cloud account and starts an agent that can run flows. `build.sh` is the harness for `docker build`. It expects five variables to be set in the environment: `PREFECT_API_KEY`, `PREFECT_WORKSPACE`, `PREFECT_API_URL`, `CLUSTER_NAME` (the name of the Dataproc cluster), and `REGION` (the region of the Dataproc cluster).

The heart of the `Dockerfile` is `run.sh`, which logs into a Prefect Cloud account, sets the Prefect API URL, builds, schedules, and applies deployments, and starts a Prefect agent. For this to work, you must have previously configured remote storage for the flow code, which is probably easiest to do in the Prefect Cloud UI.

Push the image you build to Docker Hub. `compute/main.tf` will create a container from this image and run it on the Google Cloud Engine VM it provisions.

### Running Flows

The deployment built by the Docker container auto schedules flow runs based on the scheduling parameters in the deployment scripts, and the Prefect agent running in the container runs them. You can also run flows from the Prefect Cloud UI.

## Running the Pipeline End-to-End

```bash
make up IMAGE_NAME=docker_image_name_with_tag
```

## Data

- [Open Library Data Dumps](https://openlibrary.org/developers/dumps)
- [Open Library JSON Schemas](https://github.com/internetarchive/openlibrary-client/tree/master/olclient/schemata)

## TODO

- [ ] Running `docker history blackerby/open_library_pipeline` will display sensitive information (e.g., `PREFECT_API_KEY`). Look into how to pass secrets when building a Docker image.
