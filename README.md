# Open Library Pipeline

Workspace for [DataTalksClub's Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Infrastructure

### Cloud Storage

To set up the Google Cloud Storage data lake and Prefect remote storage from the root directory, run

```bash
make apply-storage
```

and follow the prompts.

It is reasonable to leave the data lake up and running, but if for some reason it needs to be removed, run

```bash
make destroy-storage
```

in the root directory.

### Cloud Compute

To set up the Google Compute Engine VM that runs a Docker container for this project from the root directory, run

```bash
make apply-compute
```

and follow the prompts.

It is reasonable to take down the VM when it is not in use. To do so, run

```bash
make destroy-compute
```

in the root directory.

## Orchestration

The `Dockerfile` builds an image that connects to a Prefect Cloud account and starts an agent that can run flows. `build.sh` is the harness for `docker build`. It expects three variables (`PREFECT_API_KEY`, `PREFECT_WORKSPACE`, and `PREFECT_API_URL`) to be set in the environment and expects four command line arguments: `SCRIPT_NAME`, `FLOW_TAG`, `DEPLOYMENT_NAME`, and `INTERVAL` (in seconds).

The heart of the `Dockerfile` is `run.sh`, which logs into a Prefect Cloud account, sets the Prefect API URL, builds, schedules, and applies a deployment, and starts a Prefect agent. For this to work, you must have previously configured remote storage for the flow code, which is probably easiest to do in the Prefect Cloud UI.

Push the image you build to Docker Hub. `compute/main.tf` will create a container from this image and run it on the Google Cloud Engine VM it provisions.

### Running Flows

The deployment built by the Docker container auto schedules flow runs based on the value of the `INTERVAL` parameter, and the Prefect agent running in the container runs them. You can also run flows from the Prefect Cloud UI.

## Running the Pipeline End-to-End

```bash
  make up SCRIPT_NAME=script_name.py FLOW_TAG=flow_name DEPLOYMENT_NAME=deployment_name INTERVAL=a_number IMAGE_NAME=docker_image_name_with_tag
```

## Taking the Pipeline Down

```bash
make down DEPLOYMENT_NAME="flow_name/deployment_name"
```

## Data

- [Open Library Data Dumps](https://openlibrary.org/developers/dumps)
- [LibrariesHacked Open Library database](https://github.com/LibrariesHacked/openlibrary-search)
  - Interesting examples of PostgreSQL JSON syntax
- [Open Library JSON Schemas](https://github.com/internetarchive/openlibrary-client/tree/master/olclient/schemata)

### Initial Exploration

[exploration.ipynb](./exploration.ipynb) contains a sketch of how to use Spark to process the raw Open Library data.

## Resources

### Potentially Useful Python Libraries

- [gzip](https://docs.python.org/3/library/gzip.html)

## Up Next

- [ ] Investigate how to upload large files to GCS without saving them locally.

## TODO

- [ ] Running `docker history blackerby/open_library_pipeline` will display sensitive information (e.g., `PREFECT_API_KEY`). Look into how to pass secrets when building a Docker image.
- [ ] Experiment with running an actual data processing flow.
- [ ] Look into
  - [x] Performing initial flow runs in Docker container
  - [x] Building and applying deployments in Docker container
  - [ ] Prefect Cloud best practices for Docker containers
- [ ] Investigate `.prefectignore` best practices
