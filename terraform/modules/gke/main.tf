resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.location
  network  = var.vpc_id
  subnetwork = var.subnet_id

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  # Configure authorized networks
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "67.176.9.173/32"
      display_name = "My IP"
    }
  }

  # Add tags for firewall rules
  node_config {
    machine_type = var.machine_type
    disk_size_gb = var.disk_size_gb
    disk_type    = var.disk_type
    image_type   = var.image_type
    tags         = ["gke-${var.cluster_name}", "gke-cluster"]
  }

  # Disable deletion protection
  deletion_protection = false
}

# Create a node pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.cluster_name}-node-pool"
  location   = var.location
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    machine_type = var.machine_type
    disk_size_gb = var.disk_size_gb
    disk_type    = var.disk_type
    image_type   = var.image_type
    tags         = ["gke-${var.cluster_name}", "gke-cluster"]
  }
} 