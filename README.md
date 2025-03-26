# Datadog Agent Sandbox

This repository contains a sandbox environment for testing and experimenting with Datadog agents across different deployment scenarios. It includes configurations for both bare-metal and Kubernetes (GKE) environments, along with a sample FastAPI application for testing.

## Project Structure

```
.
├── apps/
│   └── fastapi_app/         # Sample FastAPI application for testing
├── dd-agent/
│   ├── bare-metal/         # Bare-metal Datadog agent configurations
│   ├── gke/               # GKE-specific Datadog agent configurations
│   └── setup.sh           # Setup script for Datadog agent deployment
└── utils/
    └── redis/             # Redis utility configurations
```

## Prerequisites

- Kubernetes cluster (for GKE deployment)
- Datadog account and API key
- Docker (for local development)
- Python 3.8+ (for FastAPI application)

## Setup

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

### FastAPI Application

1. Navigate to the FastAPI application directory:
   ```bash
   cd apps/fastapi_app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Components

### FastAPI Application
A sample FastAPI application that can be used to test Datadog monitoring. It includes:
- Basic API endpoints
- Redis integration
- Environment configuration using pydantic-settings

### Datadog Agent Configurations
- **Bare-metal**: Configuration for running Datadog agent directly on a host
- **GKE**: Kubernetes-specific configurations for deploying Datadog agent in a GKE cluster

## Development

The project is structured to support different deployment scenarios and testing environments. Each component can be developed and tested independently.

## License

This project is licensed under the terms specified in the LICENSE file.
