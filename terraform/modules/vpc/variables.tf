variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "region" {
  description = "Region where the VPC will be created"
  type        = string
}

variable "subnet_cidr" {
  description = "CIDR range for the subnet"
  type        = string
  default     = "10.0.0.0/24"
}

variable "auto_create_subnetworks" {
  description = "Whether to create default subnetworks"
  type        = bool
  default     = false
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
}

variable "allowed_ip" {
  description = "IP address to allow access from"
  type        = string
} 