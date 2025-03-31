output "cluster_name" {
  description = "The name of the GKE cluster"
  value       = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  description = "The IP address of the GKE cluster master"
  value       = google_container_cluster.primary.endpoint
}

output "cluster_ca_certificate" {
  description = "The public certificate that is the root of trust for the GKE cluster"
  value       = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
}

output "cluster_zone" {
  description = "The zone where the GKE cluster is deployed"
  value       = google_container_cluster.primary.location
} 