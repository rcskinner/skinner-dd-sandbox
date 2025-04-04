provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

module "vpc" {
  source = "./modules/vpc"

  vpc_name     = "skinner-otel-demo-vpc"
  subnet_cidr  = "10.0.0.0/24"
  region       = var.region
  cluster_name = var.cluster_name
  allowed_ip   = var.allowed_ip
}

module "gke" {
  source = "./modules/gke"

  project_id   = var.project_id
  location     = var.zone
  cluster_name = var.cluster_name
  vpc_id       = module.vpc.vpc_id
  subnet_id    = module.vpc.subnet_id
  environment  = var.environment
  vpc_cidr     = module.vpc.subnet_cidr
  node_count   = var.node_count

  depends_on = [module.vpc]
}

# Configure kubectl context after cluster creation
resource "null_resource" "configure_kubectl" {
  depends_on = [module.gke]

  provisioner "local-exec" {
    command = "gcloud container clusters get-credentials ${module.gke.cluster_name} --zone ${var.zone}"
  }
}

#TODO: Add Datadog Agent Secrets at provision time
# Add your GCP resources here 