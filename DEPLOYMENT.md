# FinGemma Deployment Guide

This document explains how to deploy the FinGemma application using Docker.

## Overview

FinGemma is a finance-focused language model application that can run in two modes:
- **UI Mode**: Gradio web interface for interactive conversations
- **API Mode**: FastAPI REST endpoints for programmatic access

The application includes a pre-trained Gemma 3 270M model fine-tuned for finance use cases.

## Quick Start

### Option 1: Pull from Docker Hub (Recommended)
```bash
# Pull the pre-built image
docker pull huseyincavus/fingemma:latest

# Run UI Mode
docker run -p 7860:7860 huseyincavus/fingemma:latest

# Run API Mode
docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest
```

### Option 2: Build from Source
```bash
# Build the Docker Image
docker build -t fingemma:latest .

# Run UI Mode
docker run -p 7860:7860 fingemma:latest

# Run API Mode
docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 fingemma:latest
```

Access the web interface at: http://localhost:7860

## Transferring the Container to Other Systems

Since the container is now available on Docker Hub, deployment is much simpler:

### Option 1: Docker Hub (Recommended - Easy)
```bash
# On any system with Docker installed
docker pull huseyincavus/fingemma:latest
docker run -p 7860:7860 huseyincavus/fingemma:latest
```

### Option 2: Save/Load Docker Image (for Offline Transfer)
```bash
# On source system - export image to tar file
docker save huseyincavus/fingemma:latest > fingemma-image.tar

# Transfer the tar file to target system (scp, usb, etc.)
scp fingemma-image.tar user@target-system:/path/to/destination/

# On target system - load the image
docker load < fingemma-image.tar
docker run -p 7860:7860 huseyincavus/fingemma:latest
```

### Option 3: Build from Source (if you have the source code)
```bash
# On target system with source code
git clone <your-repo>
cd FinGemma
docker build -t fingemma:latest .
docker run -p 7860:7860 fingemma:latest
```

## Using Docker Compose

### Run UI Mode
```bash
docker-compose --profile ui up
```

### Run API Mode
```bash
docker-compose --profile api up
```

### Run Default (UI Mode)
```bash
docker-compose --profile default up
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_MODE` | `ui` | Application mode: `ui` or `api` |
| `PORT` | `7860` | Port to run the application on |
| `SERVER_NAME` | `127.0.0.1` | Server bind address (use `0.0.0.0` for containers) |
| `LOCAL_MODEL_PATH` | (auto-detected) | Path to local model files |
| `MODEL_ID` | `huseyincavus/gemma-3-270m-finance-merged` | Model identifier |

## API Endpoints

When running in API mode, the following endpoints are available:

### Health Check
```bash
curl http://localhost:8000/health
```

### Generate Text
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is EBITDA?",
    "max_new_tokens": 128,
    "temperature": 0.7,
    "top_p": 0.9,
    "stream": false
  }'
```

### Streaming Generation
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain compound interest",
    "max_new_tokens": 128,
    "temperature": 0.7,
    "top_p": 0.9,
    "stream": true
  }'
```

## Running on Different Systems

### Prerequisites
- Docker installed and running
- At least 8GB RAM available
- 5GB free disk space
- Network access for initial setup

### Windows

#### Docker Desktop Installation
1. **Download and Install Docker Desktop**: 
   - Visit [docker.com](https://www.docker.com/products/docker-desktop/)
   - Download Docker Desktop for Windows
   - Run the installer and follow the setup wizard
   - Restart your computer when prompted

2. **Verify Installation**:
   ```powershell
   docker --version
   docker info
   ```

3. **Run FinGemma**:
   ```powershell
   # Pull the image from Docker Hub
   docker pull huseyincavus/fingemma:latest
   
   # UI Mode (Web Interface)
   docker run -p 7860:7860 huseyincavus/fingemma:latest
   
   # API Mode (REST API)
   docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest
   ```

4. **Access the Application**:
   - UI Mode: Open browser to http://localhost:7860
   - API Mode: Access endpoints at http://localhost:8000

### macOS

#### Docker Desktop Installation (Recommended)
1. **Download and Install Docker Desktop**:
   - Visit [docker.com](https://www.docker.com/products/docker-desktop/)
   - Download Docker Desktop for Mac (Intel or Apple Silicon)
   - Drag Docker.app to Applications folder
   - Launch Docker Desktop and complete setup

2. **Verify Installation**:
   ```bash
   docker --version
   docker info
   ```

3. **Run FinGemma**:
   ```bash
   # Pull the image from Docker Hub
   docker pull huseyincavus/fingemma:latest
   
   # UI Mode (Web Interface)
   docker run -p 7860:7860 huseyincavus/fingemma:latest
   
   # API Mode (REST API)
   docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest
   ```

4. **Access the Application**:
   - UI Mode: Open browser to http://localhost:7860
   - API Mode: Access endpoints at http://localhost:8000

### Ubuntu/Debian Linux

#### Docker Installation
1. **Update Package Index**:
   ```bash
   sudo apt update
   ```

2. **Install Docker**:
   ```bash
   # Install dependencies
   sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release
   
   # Add Docker GPG key
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   
   # Add Docker repository
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
   # Install Docker Engine
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

3. **Start Docker and Add User to Docker Group**:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   ```
   **Note**: Log out and back in for group changes to take effect

4. **Verify Installation**:
   ```bash
   docker --version
   docker info
   ```

5. **Run FinGemma**:
   ```bash
   # Pull the image from Docker Hub
   docker pull huseyincavus/fingemma:latest
   
   # UI Mode (Web Interface)
   docker run -p 7860:7860 huseyincavus/fingemma:latest
   
   # API Mode (REST API)
   docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 huseyincavus/fingemma:latest
   ```

6. **Access the Application**:
   - UI Mode: Open browser to http://localhost:7860
   - API Mode: Access endpoints at http://localhost:8000

## Common Docker Commands

### Managing Containers
```bash
# Run in background (detached mode)
docker run -d --name fingemma-ui -p 7860:7860 fingemma:latest

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs fingemma-ui

# Stop a container
docker stop fingemma-ui

# Remove a container
docker rm fingemma-ui

# Restart a container
docker restart fingemma-ui
```

### Useful Options
```bash
# Run with custom environment variables
docker run -p 7860:7860 -e SERVER_NAME=0.0.0.0 -e PORT=7860 fingemma:latest

# Run with volume mounting (for logs or data persistence)
docker run -p 7860:7860 -v /path/to/logs:/app/logs fingemma:latest

# Run with memory limits
docker run -p 7860:7860 --memory=8g fingemma:latest

# Run with automatic restart
docker run -d --restart unless-stopped -p 7860:7860 fingemma:latest
```

### Cloud Platforms

#### AWS EC2
1. **Launch EC2 instance** (t3.large or larger recommended)
2. **Install Docker**:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo systemctl start docker
   sudo usermod -aG docker ec2-user
   ```

3. **Run with public access**:
   ```bash
   # UI Mode - accessible from internet
   docker run -p 7860:7860 -e SERVER_NAME=0.0.0.0 fingemma:latest
   
   # API Mode
   docker run -p 8000:8000 -e APP_MODE=api -e PORT=8000 fingemma:latest
   ```

4. **Configure Security Group**: Allow inbound traffic on ports 7860/8000

#### Google Cloud Platform
1. **Create Compute Engine instance** (n1-standard-2 or larger)
2. **Install Docker**:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   ```

3. **Run with external IP access**:
   ```bash
   docker run -p 7860:7860 -e SERVER_NAME=0.0.0.0 fingemma:latest
   ```

4. **Configure Firewall**: Allow tcp:7860 and tcp:8000

#### Azure VM
1. **Create Virtual Machine** (Standard_B2s or larger)
2. **Install Docker**:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo usermod -aG docker azureuser
   ```

3. **Run the container** (same as GCP)
4. **Configure NSG**: Allow inbound rules for ports 7860/8000

#### DigitalOcean Droplet
1. **Create Droplet** (2GB RAM minimum)
2. **One-click Docker installation** or manual install:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Run the container**:
   ```bash
   docker run -p 7860:7860 -e SERVER_NAME=0.0.0.0 fingemma:latest
   ```

### Container Orchestration

#### Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml fingemma
```

#### Kubernetes
```yaml
# fingemma-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fingemma
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fingemma
  template:
    metadata:
      labels:
        app: fingemma
    spec:
      containers:
      - name: fingemma
        image: fingemma:latest
        ports:
        - containerPort: 7860
        env:
        - name: APP_MODE
          value: "ui"
        - name: SERVER_NAME
          value: "0.0.0.0"
---
apiVersion: v1
kind: Service
metadata:
  name: fingemma-service
spec:
  selector:
    app: fingemma
  ports:
  - port: 80
    targetPort: 7860
  type: LoadBalancer
```

Deploy with:
```bash
kubectl apply -f fingemma-deployment.yaml
```

## Production Deployment

For production deployment, consider:

1. **Resource Requirements**: The model requires sufficient CPU/memory. GPU acceleration available if CUDA is supported.

2. **Security**: 
   - Run containers with non-root users
   - Use proper network isolation
   - Implement authentication if needed
   - Use HTTPS with reverse proxy (nginx/traefik)

3. **Scaling**:
   - Multiple API instances behind a load balancer
   - Horizontal scaling with container orchestration

4. **Monitoring**:
   - Health check endpoints for monitoring
   - Log aggregation for troubleshooting

## Container Details

- **Base Image**: `python:3.10-slim`
- **Model Size**: ~550MB (included in container)
- **Container Size**: ~2.5GB total
- **Exposed Ports**: 7860 (UI), 8000 (API)

## Troubleshooting

### Container Won't Start
- Check logs: `docker logs <container-name>`
- Verify sufficient memory/disk space
- Ensure ports are not in use

### Model Loading Issues
- The model is embedded in the container
- Check `LOCAL_MODEL_PATH` environment variable
- Verify model files are present in container

### Performance Issues
- Consider enabling GPU support if available
- Adjust generation parameters (temperature, max_tokens)
- Monitor resource usage

## Development

To run in development mode without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run UI mode
python start.py

# Run API mode
APP_MODE=api python start.py
```
