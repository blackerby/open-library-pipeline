terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "e2-medium"
  tags         = ["spark", "prefect"]

  boot_disk {
    auto_delete = true
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    subnetwork = "projects/open-library-pipeline/regions/us-east4/subnetworks/default"
  }

  metadata = {
    gce-container-declaration = module.gce-advanced-container.metadata_value
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }
}

module "gce-advanced-container" {
  source = "terraform-google-modules/container-vm/google"
  container = {
    image = "docker.io/prefect:2-python3.10"
  }

  restart_policy = "Always"
}
