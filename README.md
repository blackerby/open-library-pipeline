# Open Library Pipeline

Workspace for [DataTalksClub's Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Infrastructure

### Cloud Storage

To set up the Google Cloud Storage data lake, from the root directory

1. `cd storage`
2. `terraform apply`
3. Enter `yes`

It is reasonable to leave the data lake up and running, but if for some reason it needs to be removed, run `terraform destroy` in the `storage` directory.

### Cloud Compute

To set up the Google Compute Engine VM that runs a Prefect agent, from the root directory

1. `cd compute`
2. `terraform apply`
3. Enter `yes`

It is reasonable to take down the VM when it is not in use. To do so, run `terraform destroy` in the compute directory.

## Orchestration

The project uses Prefect Cloud to run flows instead of a local Prefect installation. Follow these steps to set up Prefect Cloud to run flows.

1. Log in to Prefect Cloud with `prefect cloud login`
2. Run flows locally to register them in the cloud UI. For example, from the root directory `python flows/hello.py`
3. In the `flows` directory, run `prefect deployment build hello.py:hello --name hello-world --storage-block gcs/open-library-pipeline-gcs-storage` to create a deployment and store the flow code in the cloud
4. Apply the deployment with `prefect deployment apply flows/hello-deployment.yaml`

### Prefect Agent Container

The `Dockerfile` builds an image that connects to a Prefect Cloud account and starts an agent that can run flows. Use `docker build --build-arg PREFECT_API_KEY=$PREFECT_API_KEY --build-arg PREFECT_API_URL=$PREFECT_API_URL --build-arg PREFECT_WORKSPACE=$PREFECT_WORKSPACE -t blackerby/open_library_pipeline .` to build the image. Use `docker push blackerby/open_library_pipeline:latest` to push the image to Docker Hub. `compute/main.tf` will create a container from this image and run it on the Google Cloud Engine VM it provisions.

### Running Flows

To run using deployments, use the Prefect Cloud UI.

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
  - [ ] Performing initial flow runs in Docker container
  - [ ] Building and applying deployments in Docker container
  - [ ] Prefect Cloud best practices for Docker containers
- [ ] Investigate `.prefectignore` best practices
