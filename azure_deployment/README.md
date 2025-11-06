# Azure Deployment Guide for CroweLogic-Pharma

This directory contains configuration files and scripts for deploying the CroweLogic-Pharma pharmaceutical AI model to Microsoft Azure.

## Deployment Options

### 1. Azure Container Instances (ACI)
- **Best for**: Quick deployment, development, testing
- **Cost**: Pay-per-use, lower cost for intermittent usage
- **Resources**: 4 CPU cores, 16GB RAM
- **Scaling**: Manual, single container

### 2. Azure Machine Learning (Azure ML)
- **Best for**: Production, research, model training
- **Cost**: Higher, but includes ML tools and monitoring
- **Resources**: Configurable compute clusters
- **Scaling**: Automatic scaling based on demand

## Prerequisites

### Required Tools
- **Azure CLI**: [Installation Guide](https://docs.microsoft.com/cli/azure/install-azure-cli)
- **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
- **Python 3.8+**: With pip and virtualenv

### Azure Account
- Active Azure subscription
- Appropriate permissions to create resources
- Subscription ID

## Quick Start

### Option 1: Deploy to Azure Container Instances (Recommended for testing)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create configuration
python azure_deployment/deploy_azure.py --config

# 3. Edit deployment_config.json with your Azure details
# Update: subscription_id, resource_group, location, acr_name

# 4. Deploy
python azure_deployment/deploy_azure.py --type aci
```

### Option 2: Deploy to Azure Machine Learning

```bash
# 1. Install Azure ML SDK
pip install azure-ai-ml azure-identity azureml-core

# 2. Create configuration
python azure_deployment/deploy_azure.py --config

# 3. Deploy
python azure_deployment/deploy_azure.py --type azureml
```

## Detailed Deployment Steps

### 1. Prepare Configuration

Edit `deployment_config.json`:

```json
{
  "subscription_id": "your-subscription-id",
  "resource_group": "crowelogic-pharma-rg",
  "location": "eastus",
  "acr_name": "crowelogicpharmaacr",
  "aci_name": "crowelogic-pharma-aci",
  "model_name": "CroweLogic-Pharma",
  "model_version": "latest",
  "compute": {
    "cpu": 4,
    "memory_gb": 16,
    "gpu_count": 0
  }
}
```

### 2. Deploy to Azure Container Instances

The deployment script will:
1. Login to Azure
2. Create resource group
3. Create Azure Container Registry (ACR)
4. Build Docker image with CroweLogic-Pharma model
5. Push image to ACR
6. Deploy container to ACI

```bash
python azure_deployment/deploy_azure.py --type aci
```

After deployment completes, note the endpoint:
- **Model Endpoint**: `http://<your-endpoint>:11434`
- **API Endpoint**: `http://<your-endpoint>:8000`

### 3. Verify Deployment

Test the deployed model:

```bash
# Query the model
curl -X POST http://<your-endpoint>:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma",
    "prompt": "What are the therapeutic applications of hericenones from Lion'\''s Mane mushroom?",
    "stream": false
  }'
```

## Cost Estimation

### Azure Container Instances
- **Configuration**: 4 vCPU, 16GB RAM
- **Estimated Cost**: ~$200-300/month (continuous running)
- **Optimization**: Use Azure Functions for on-demand execution

### Azure Machine Learning
- **Development**: ~$100-200/month (small compute instance)
- **Production**: ~$500-1000/month (with auto-scaling)
- **Training**: Pay-per-use for GPU compute

## Scaling and Optimization

### Horizontal Scaling (Multiple Instances)

For Azure Container Instances:
```bash
az container create \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci-2 \
  --file azure-container-instance.yaml
```

### Vertical Scaling (More Resources)

Edit `azure-container-instance.yaml`:
```yaml
resources:
  requests:
    cpu: 8.0  # Increased from 4
    memoryInGb: 32.0  # Increased from 16
```

## Monitoring and Logging

### Enable Azure Monitor

```bash
# Enable diagnostics
az monitor diagnostic-settings create \
  --resource <container-resource-id> \
  --name crowelogic-pharma-diagnostics \
  --logs '[{"category": "ContainerInstanceLog", "enabled": true}]' \
  --metrics '[{"category": "AllMetrics", "enabled": true}]'
```

### View Logs

```bash
# Real-time logs
az container logs \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --follow

# Application Insights integration
# Add Application Insights key to environment variables
```

## Security Best Practices

### 1. Network Security

```bash
# Deploy in Virtual Network
az container create \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --vnet <vnet-name> \
  --subnet <subnet-name>
```

### 2. Managed Identity

Enable managed identity for secure access to Azure resources:

```bash
az container create \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --assign-identity
```

### 3. Private Container Registry

Use ACR with private access:

```bash
# Enable admin user (development only)
az acr update \
  --name crowelogicpharmaacr \
  --admin-enabled false

# Use managed identity or service principal for production
```

## Troubleshooting

### Issue: Container fails to start

**Solution**: Check logs
```bash
az container logs \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci
```

### Issue: Out of memory errors

**Solution**: Increase memory allocation in YAML
```yaml
memoryInGb: 32.0  # Increase from 16
```

### Issue: Image pull errors

**Solution**: Verify ACR credentials
```bash
az acr credential show --name crowelogicpharmaacr
```

## API Integration

### Python Client Example

```python
import requests
import json

ENDPOINT = "http://<your-endpoint>:11434/api/generate"

def query_crowelogic_pharma(prompt):
    payload = {
        "model": "CroweLogic-Pharma",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(ENDPOINT, json=payload)
    result = response.json()

    return result['response']

# Example usage
answer = query_crowelogic_pharma(
    "How do I use ChEMBL data for drug target identification?"
)
print(answer)
```

### REST API Endpoints

- **Generate**: `POST /api/generate` - Generate text from prompt
- **Chat**: `POST /api/chat` - Multi-turn conversation
- **Embeddings**: `POST /api/embeddings` - Generate embeddings
- **Models**: `GET /api/tags` - List available models

## Updating the Deployment

### Update Model

```bash
# 1. Rebuild image with new model
python scripts/build_crowelogic_pharma.py

# 2. Rebuild and push Docker image
az acr build \
  --registry crowelogicpharmaacr \
  --image crowelogic-pharma:latest \
  --file azure_deployment/Dockerfile \
  .

# 3. Restart container
az container restart \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci
```

### Update Configuration

```bash
# Delete existing deployment
az container delete \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --yes

# Redeploy with new configuration
python azure_deployment/deploy_azure.py --type aci
```

## Cleanup

### Delete Deployment

```bash
# Delete container instance
az container delete \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --yes

# Delete entire resource group (WARNING: deletes everything)
az group delete \
  --name crowelogic-pharma-rg \
  --yes
```

## Additional Resources

- [Azure Container Instances Documentation](https://docs.microsoft.com/azure/container-instances/)
- [Azure Machine Learning Documentation](https://docs.microsoft.com/azure/machine-learning/)
- [Azure Container Registry Documentation](https://docs.microsoft.com/azure/container-registry/)
- [Ollama Docker Documentation](https://github.com/ollama/ollama/blob/main/docs/docker.md)

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Azure service health status
3. Consult Azure documentation
4. Contact Azure support

---

**Last Updated**: 2025-11-06
**Version**: 1.0.0
