variable "project" {}

variable "credentials_file" {}

variable "region" {
  default = "us-east4"
}

variable "zone" {
  default = "us-east4-c"
}

variable "CLUSTER_NAME" {
  type        = string
  description = "Google Dataproc cluster name"
}

variable "CLUSTER_REGION" {
  type        = string
  description = "GCP region for Dataproc cluster"
}
