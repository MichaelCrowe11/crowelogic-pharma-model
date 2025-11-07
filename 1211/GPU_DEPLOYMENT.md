# GPU-Accelerated Deployment Guide

Complete guide for deploying CroweLogic-Pharma with GPU acceleration for maximum performance.

## GPU Benefits

### Performance Comparison

| Model Size | CPU (Cores) | Time per Query | GPU (VRAM) | Time per Query | Speedup |
|-----------|-------------|----------------|------------|----------------|---------|
| 1B (mini) | 4 cores | ~2 sec | 4GB | ~0.5 sec | 4x |
| 3B (standard) | 8 cores | ~5 sec | 8GB | ~1 sec | 5x |
| 8B (pro) | 16 cores | ~15 sec | 16GB | ~2 sec | 7-8x |
| 70B (enterprise) | 64 cores | ~60 sec | 48GB | ~8 sec | 7-8x |

---

## Option 1: Docker with GPU (Local/Server)

### Prerequisites
- NVIDIA GPU (RTX 3060+, RTX 4090, A100, etc.)
- NVIDIA drivers installed
- Docker with NVIDIA Container Toolkit

### Setup

1. **Install NVIDIA Container Toolkit**:
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

2. **Build and Run**:
```bash
cd /path/to/crowelogic-pharma-model

# Build GPU-enabled image
docker build -f azure_deployment/Dockerfile-gpu -t crowelogic-pharma:gpu .

# Run with GPU
docker run -d \
  --gpus all \
  --name crowelogic-pharma \
  -p 11434:11434 \
  -v ollama-data:/root/.ollama \
  crowelogic-pharma:gpu
```

3. **Using Docker Compose**:
```bash
# Start with GPU support
docker-compose -f azure_deployment/docker-compose-gpu.yml up -d

# View logs
docker-compose -f azure_deployment/docker-compose-gpu.yml logs -f

# Stop
docker-compose -f azure_deployment/docker-compose-gpu.yml down
```

---

## Option 2: Azure GPU VM

### Recommended Azure VM Sizes

| VM Size | GPU | VRAM | RAM | vCPUs | Recommended Model | Cost/Month* |
|---------|-----|------|-----|-------|-------------------|-------------|
| **NC6s_v3** | V100 | 16GB | 112GB | 6 | Pro (8B) | ~$1,200 |
| **NC12s_v3** | V100 | 32GB | 224GB | 12 | Enterprise (70B) | ~$2,400 |
| **NC24s_v3** | 4x V100 | 64GB | 448GB | 24 | Enterprise (70B) multi-GPU | ~$4,800 |
| **NC4as_T4_v3** | T4 | 16GB | 28GB | 4 | Pro (8B) | ~$400 |

*Approximate costs for continuous running

### Deployment Steps

1. **Create GPU VM**:
```bash
# Create resource group
az group create --name crowelogic-pharma-gpu-rg --location eastus

# Create GPU VM
az vm create \
  --resource-group crowelogic-pharma-gpu-rg \
  --name crowelogic-pharma-vm \
  --size Standard_NC6s_v3 \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys
```

2. **Install GPU Drivers on VM**:
```bash
# SSH into VM
ssh azureuser@<vm-ip>

# Install NVIDIA drivers
sudo apt update
sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# Verify GPU (after reboot)
nvidia-smi
```

3. **Deploy Model**:
```bash
# Install Docker and NVIDIA toolkit (from Option 1)
# Then clone repo and run:
git clone <your-repo>
cd crowelogic-pharma-model

docker-compose -f azure_deployment/docker-compose-gpu.yml up -d
```

---

## Option 3: Azure Container Instances with GPU (Simpler)

### Configuration

Create `azure-container-instance-gpu.yaml`:

```yaml
apiVersion: 2019-12-01
location: eastus
name: crowelogic-pharma-gpu-aci
properties:
  containers:
  - name: crowelogic-pharma-gpu
    properties:
      image: <your-acr>.azurecr.io/crowelogic-pharma:gpu
      resources:
        requests:
          cpu: 4
          memoryInGb: 16
          gpu:
            count: 1
            sku: K80  # or V100, P100
      ports:
      - port: 11434
        protocol: TCP
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 11434
  sku: Standard
tags:
  project: CroweLogic-Pharma-GPU
```

### Deploy:
```bash
az container create \
  --resource-group crowelogic-pharma-rg \
  --file azure-container-instance-gpu.yaml
```

---

## Option 4: Azure Machine Learning Compute

### Best for Research Workloads

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute

# Connect to workspace
ml_client = MLClient.from_config()

# Create GPU compute cluster
gpu_compute = AmlCompute(
    name="crowelogic-gpu-cluster",
    size="Standard_NC6s_v3",  # V100 GPU
    min_instances=0,
    max_instances=4,
    idle_time_before_scale_down=600
)

ml_client.compute.begin_create_or_update(gpu_compute)
```

---

## Choosing GPU Configuration

### By Budget

**Budget: $100-400/month**
- Use **CPU Standard (3B)** or small T4 GPU
- Good enough for most use cases
- Azure VM: Standard_D4s_v3 (CPU) or NC4as_T4_v3 (GPU)

**Budget: $400-1,200/month**
- Use **Pro (8B) with V100 GPU**
- Excellent performance
- Azure VM: NC6s_v3

**Budget: $1,200-2,400/month**
- Use **Enterprise (70B) with V100/A100**
- Maximum quality
- Azure VM: NC12s_v3

### By Use Case

| Use Case | Recommended Setup |
|----------|------------------|
| **Development** | CPU 3B or Mini GPU 1B |
| **API Production** | GPU 8B (T4 or V100) |
| **Research** | GPU 70B (A100) |
| **High-Volume API** | Multi-GPU 8B load balanced |

---

## Performance Optimization

### GPU Utilization

Monitor GPU usage:
```bash
# In container
nvidia-smi -l 1

# Docker stats with GPU
docker stats crowelogic-pharma
```

### Batch Processing

For multiple queries, use batch mode:
```python
import requests

# Send multiple queries in parallel
queries = [
    "What are hericenones?",
    "Explain IC50 values",
    "SAR analysis methods"
]

# Process in parallel (GPU handles efficiently)
for query in queries:
    requests.post('http://localhost:11434/api/generate',
                  json={"model": "CroweLogic-Pharma:pro", "prompt": query})
```

---

## Cost Optimization

### Auto-Scaling

Set up auto-scaling to reduce costs:

```yaml
# Azure Container Apps with auto-scaling
properties:
  scale:
    minReplicas: 0  # Scale to zero when idle
    maxReplicas: 3
    rules:
    - name: http-scaling
      http:
        metadata:
          concurrentRequests: '10'
```

### Spot Instances

Use Azure Spot VMs for 70-90% cost savings:

```bash
az vm create \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-spot \
  --size Standard_NC6s_v3 \
  --priority Spot \
  --max-price 0.50 \  # Max hourly price
  --eviction-policy Deallocate
```

### Scheduled Shutdowns

Auto-shutdown during off-hours:

```bash
# Azure automation to shut down VMs at 6 PM
az vm auto-shutdown \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-vm \
  --time 1800
```

---

## Monitoring GPU Performance

### Setup Monitoring

```bash
# Install nvidia_gpu_prometheus_exporter
docker run -d --rm \
  --gpus all \
  -p 9835:9835 \
  nvidia/cuda:12.1.0-base-ubuntu22.04 \
  nvidia_gpu_prometheus_exporter
```

### Key Metrics

- **GPU Utilization**: Target 70-90% for efficiency
- **VRAM Usage**: Should not exceed 90%
- **Temperature**: Keep under 80°C
- **Power Draw**: Monitor for cost optimization

---

## Quick Start Commands

### For Current Testing (Codespaces - CPU):
```bash
ollama pull llama3.2:1b
ollama create CroweLogic-Pharma:mini -f models/CroweLogicPharmaModelfile-mini
ollama run CroweLogic-Pharma:mini
```

### For Production (GPU - Local Docker):
```bash
docker-compose -f azure_deployment/docker-compose-gpu.yml up -d
```

### For Production (GPU - Azure):
```bash
# Deploy GPU VM and run Docker container
python azure_deployment/deploy_azure_gpu.py
```

---

## Troubleshooting

### GPU Not Detected
```bash
# Check NVIDIA drivers
nvidia-smi

# Check Docker GPU access
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Out of Memory
- Reduce context window (`num_ctx`)
- Use smaller model variant
- Enable model quantization
- Add more VRAM

### Slow Performance
- Check GPU utilization (should be >70%)
- Verify using GPU (not CPU fallback)
- Increase `num_batch` parameter
- Check for CPU bottleneck

---

**Recommendation for You:**

1. **NOW (Codespaces)**: Use **Mini (1B)** CPU version
2. **Local Testing**: Use **Standard (3B)** CPU version
3. **Production**: Deploy **Pro (8B)** with GPU on Azure NC4as_T4_v3

This gives you 7-8x faster responses and can handle 10-20 simultaneous queries!
