terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Create VPC
resource "google_compute_network" "vpc" {
  name                    = var.vpc_name
  auto_create_subnetworks = false
}

# Create Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.vpc_name}-subnet"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.vpc.id
}

# Firewall rules for GKE
resource "google_compute_firewall" "allow_internal" {
  name    = "${var.vpc_name}-allow-internal"
  network = google_compute_network.vpc.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  source_ranges = [var.subnet_cidr]
  target_tags   = ["gke-cluster"]
}

# Allow access from your IP to GKE nodes
resource "google_compute_firewall" "allow_gke_access" {
  name    = "allow-gke-access"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["443", "10250"]  # Kubernetes API and kubelet ports
  }

  source_ranges = ["67.176.9.173/32"]  # Your IP
  target_tags   = ["gke-${var.cluster_name}"]
}

# Allow incoming traffic to LoadBalancer services
resource "google_compute_firewall" "allow_loadbalancer" {
  name    = "${var.vpc_name}-allow-loadbalancer"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]  # Add other ports as needed
  }

  source_ranges = ["67.176.9.173/32"]  # Your IP
  target_tags   = ["gke-${var.cluster_name}"]
} 