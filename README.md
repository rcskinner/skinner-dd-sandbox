# Datadog Agent Sandbox

This repository contains a sandbox environment for testing and experimenting with Datadog agents across different deployment scenarios. It includes configurations for both local development and Kubernetes (GKE) environments, along with infrastructure as code using Terraform.

## Project Structure

```
.
├── dd-agent/              # Datadog agent configurations and setup
│   ├── gke/               # GKE-specific Datadog agent configurations
│   ├── local-cluster/     # Local development cluster configurations
│   └── setup.sh           # Setup script for Datadog agent deployment
├── terraform/             # Infrastructure as Code for GKE clusters
└── sandboxes/             # Sample applications for testing Datadog monitoring
    ├── otel-store/        # OpenTelemetry demo store application
    │   ├── services/      # Microservices components
    │   ├── collector/     # OpenTelemetry collector configuration
    │   └── deploy/        # Kubernetes deployment manifests
    └── fastapi-redis/     # FastAPI application with Redis integration
        ├── app/           # FastAPI application code
        ├── redis/         # Redis configuration
        ├── loadtest/      # Load testing utilities
        └── deploy/        # Kubernetes deployment manifests
```

## Prerequisites

- Kubernetes cluster (for GKE deployment)
- Datadog account and API key
- Docker (for local development)
- Terraform (for infrastructure deployment)
- Google Cloud Platform account and credentials (for GKE deployment)

## Setup

### Infrastructure Setup

1. Navigate to the `terraform` directory:
   ```bash
   cd terraform
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review and modify `terraform.tfvars` with your specific values.

4. Apply the Terraform configuration:
   ```bash
   terraform plan
   terraform apply
   ```

### Datadog Agent Setup

1. Navigate to the `dd-agent` directory:
   ```bash
   cd dd-agent
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```
   This will prompt for your Datadog API key and set up the necessary Kubernetes secrets.

## Components

### Infrastructure (Terraform)
- GKE cluster configuration
- Network and security settings
- IAM roles and permissions
- Datadog agent deployment configurations

### Datadog Agent Configurations
- **GKE**: Kubernetes-specific configurations for deploying Datadog agent in a GKE cluster
- **Local Cluster**: Configuration for local development and testing

### Sample Applications (Sandboxes)
The repository includes two sample applications for testing Datadog monitoring:

1. **OpenTelemetry Store Demo**
   - A microservices-based e-commerce application
   - Demonstrates OpenTelemetry integration with Datadog
   - Includes multiple services with distributed tracing
   - Uses OpenTelemetry Collector for telemetry data

2. **FastAPI Redis Application**
   - A FastAPI application with Redis integration
   - Demonstrates application performance monitoring
   - Includes load testing capabilities
   - Shows Redis integration monitoring

These sandbox applications provide real-world scenarios for testing and validating Datadog monitoring capabilities.

## Development

The project supports multiple deployment scenarios:
- Local development using Docker and Kubernetes
- GKE-based production-like environment
- Infrastructure as Code using Terraform

Each component can be developed and tested independently. The Terraform configurations provide a consistent infrastructure setup across different environments.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the terms specified in the LICENSE file.
