variable "project_id" {
  description = "The project ID to host the cluster in"
  type        = string
}

variable "location" {
  description = "The location (region or zone) to host the cluster in"
  type        = string
}

variable "cluster_name" {
  description = "The name of the cluster"
  type        = string
}

variable "vpc_id" {
  description = "The VPC ID to host the cluster in"
  type        = string
}

variable "subnet_id" {
  description = "The subnet ID to host the cluster in"
  type        = string
}

variable "environment" {
  description = "The environment this cluster will be used in"
  type        = string
}

variable "master_ipv4_cidr_block" {
  description = "The IP range for the master nodes"
  type        = string
  default     = "172.16.0.0/28"
}

variable "vpc_cidr" {
  description = "The CIDR range of the VPC"
  type        = string
  default     = "10.0.0.0/24"
}

variable "image_type" {
  description = "The image type to use for the nodes"
  type        = string
  default     = "COS_CONTAINERD"
}

variable "machine_type" {
  description = "The machine type to use for the nodes"
  type        = string
  default     = "t2a-standard-2"
}

variable "disk_size_gb" {
  description = "The size of the disk in GB"
  type        = number
  default     = 100
}

variable "disk_type" {
  description = "The type of disk to use"
  type        = string
  default     = "pd-standard"
}

variable "node_count" {
  description = "Number of nodes in the node pool"
  type        = number
} 