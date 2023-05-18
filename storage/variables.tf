locals {
  data_lake_bucket = "olp_data_lake"
  prefect_storage  = "olp_prefect_storage"
  dataproc_jobs    = "olp_dataproc_jobs"
}

variable "project" {}

variable "credentials_file" {}

variable "region" {
  default = "us-east4"
}

variable "zone" {
  default = "us-east4-c"
}

variable "storage_class" {
  default = "STANDARD"
}

variable "BQ_DATASET" {
  default = "open_library"
}
