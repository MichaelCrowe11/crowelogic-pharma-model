# Docker Deployment Guide

## Prerequisites

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop
2. Create Docker Hub account: https://hub.docker.com
3. Login to Docker Hub:
   ```bash
   docker login
   ```

## Build Docker Image

Build the image with version tags:

```bash
cd ~/crowelogic-pharma-model

# Build with both latest and version tags
docker build -t michaelcrowe/crowelogic-pharma-model:latest \
             -t michaelcrowe/crowelogic-pharma-model:v1.0 .
```

## Push to Docker Hub

Push both tags to Docker Hub:

```bash
# Push latest tag
docker push michaelcrowe/crowelogic-pharma-model:latest

# Push version tag
docker push michaelcrowe/crowelogic-pharma-model:v1.0
```

## Run Docker Container

### Option 1: Run generation directly
```bash
docker run -v $(pwd)/generated_data:/app/generated_data \
           michaelcrowe/crowelogic-pharma-model:latest \
           python3 generate_10m_fast.py
```

### Option 2: Run with docker-compose
```bash
# Generate 10M dataset
docker-compose up pharma-generator

# Evaluate quality
docker-compose up pharma-evaluator

# Interactive development
docker-compose up pharma-dev
```

### Option 3: Interactive shell
```bash
docker run -it \
           -v $(pwd)/generated_data:/app/generated_data \
           -v $(pwd)/logs:/app/logs \
           michaelcrowe/crowelogic-pharma-model:latest \
           /bin/bash
```

## Docker Hub Repository

Once pushed, your image will be available at:
- https://hub.docker.com/r/michaelcrowe/crowelogic-pharma-model

Pull from anywhere:
```bash
docker pull michaelcrowe/crowelogic-pharma-model:latest
```

## Cloud Deployment with Docker

### RunPod
1. Go to https://runpod.io
2. Select "Deploy" > "Custom Container"
3. Enter: `michaelcrowe/crowelogic-pharma-model:latest`
4. Add volume mount: `/workspace/generated_data` → `/app/generated_data`
5. Set command: `python3 generate_10m_fast.py`

### AWS ECS/Fargate
```bash
# Tag for ECR
docker tag michaelcrowe/crowelogic-pharma-model:latest \
           <account-id>.dkr.ecr.<region>.amazonaws.com/pharma-model:latest

# Push to ECR
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/pharma-model:latest
```

### Google Cloud Run
```bash
# Tag for GCR
docker tag michaelcrowe/crowelogic-pharma-model:latest \
           gcr.io/<project-id>/pharma-model:latest

# Push to GCR
docker push gcr.io/<project-id>/pharma-model:latest

# Deploy
gcloud run deploy pharma-model \
  --image gcr.io/<project-id>/pharma-model:latest \
  --platform managed \
  --region us-central1
```

## Verification

After pushing, verify the image:

```bash
# Pull fresh copy
docker pull michaelcrowe/crowelogic-pharma-model:latest

# Test run
docker run michaelcrowe/crowelogic-pharma-model:latest

# Should display available commands
```

## Image Details

- **Base Image:** Python 3.10-slim
- **Size:** ~400-500 MB (compressed)
- **Contains:** All Python scripts, requirements, documentation
- **Excludes:** Generated data files (via .dockerignore)

## Troubleshooting

**Issue:** "Cannot connect to Docker daemon"
```bash
# Start Docker Desktop application
open -a Docker
```

**Issue:** "denied: requested access to the resource is denied"
```bash
# Re-login to Docker Hub
docker logout
docker login
```

**Issue:** Image too large
- Generated data is excluded via `.dockerignore`
- Only code and requirements are included
- Data is mounted as volumes at runtime
