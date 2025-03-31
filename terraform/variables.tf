variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
  default     = "us-central1"
}

variable "vpc_name" {
  description = "The name of the VPC"
  type        = string
  default     = "skinner-otel-demo-vpc"
}

variable "subnet_name" {
  description = "The name of the subnet"
  type        = string
  default     = "skinner-otel-demo-subnet"
}

variable "cidr_range" {
  description = "The CIDR range for the subnet"
  type        = string
  default     = "10.0.0.0/24"
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  type        = string
  default     = "skinner-otel-demo-cluster"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "node_count" {
  description = "Number of nodes in the GKE cluster"
  type        = number
  default     = 1
} 