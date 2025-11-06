# CroweLogic-Pharma Deployment Guide

Complete guide for deploying the enhanced CroweLogic-Pharma pharmaceutical AI model with expanded datasets from Hugging Face and ChEMBL.

## Overview

The enhanced CroweLogic-Pharma model integrates:
- **Base pharmaceutical knowledge**: 8 expert examples
- **Mushroom cultivation expertise**: 90+ examples
- **ChEMBL drug targets**: 200+ drug target examples with bioactivity interpretation
- **Hugging Face datasets**: Integration examples for approved drugs, SMILES molecules, and protein-ligand complexes
- **Hybrid knowledge**: Mushroom-pharma integration examples

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Training Data Generation](#training-data-generation)
3. [Model Building](#model-building)
4. [Azure Deployment](#azure-deployment)
5. [API Usage](#api-usage)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Local Development Setup

### Prerequisites

```bash
# System requirements
- OS: Linux, macOS, or Windows with WSL
- RAM: 16GB minimum, 32GB recommended
- Storage: 50GB available
- Python 3.8+
- Docker (for containerization)
```

### Installation

```bash
# 1. Clone repository
git clone <your-repo-url>
cd crowelogic-pharma-model

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 4. Verify installation
ollama --version
python --version
```

---

## Training Data Generation

### Step 1: Generate Hugging Face Dataset Integration

```bash
# Run Hugging Face dataset integration
python scripts/add_huggingface_data.py

# Output: training_data/huggingface_training_data.jsonl
# Contains:
# - Drug-target interaction examples
# - SMILES interpretation guides
# - Protein-ligand binding affinity prediction
# - Biomedical image analysis examples
# - Mushroom-pharma validation workflows
```

**Key Features Added:**
- Approved drug-target dataset (1,660 drugs, 2,093 targets)
- ChEMBL SMILES molecules database integration
- Protein-ligand complexes (1M+ from SandboxAQ/SAIR)
- Biomedical parsing with Microsoft BiomedParseData
- ML pipeline examples for drug discovery

### Step 2: Enhance ChEMBL Data Integration

```bash
# Run enhanced ChEMBL integration (requires ChEMBL data file)
# Download ChEMBL targets: https://www.ebi.ac.uk/chembl/
python scripts/add_chembl_data.py

# Output: training_data/chembl_training_data.jsonl
# Contains:
# - 200+ diverse drug target examples
# - Bioactivity interpretation (IC50, EC50, Ki, Kd)
# - Structure-activity relationship (SAR) analysis
# - Compound-target matching examples
```

**Enhanced Features:**
- Therapeutic area classification (oncology, neurology, etc.)
- Bioactivity metrics interpretation
- SAR analysis methodologies
- QSAR model building examples
- Mushroom compound target prediction

### Step 3: Consolidate All Training Data

```bash
# Run consolidation pipeline
python scripts/consolidate_training_data.py

# Output:
# - training_data/crowelogic_pharma_expanded_training.jsonl
# - training_data/crowelogic_pharma_expanded_training_ollama.jsonl
# - training_data/crowelogic_pharma_expanded_training_stats.json
# - requirements.txt
```

**Pipeline Actions:**
1. Loads existing training data (mushroom + pharma)
2. Integrates new datasets (ChEMBL + Hugging Face)
3. Deduplicates examples
4. Validates quality
5. Generates statistics
6. Saves consolidated dataset

**Expected Output:**
```
Total Examples: 300+
Average Prompt Length: 80-100 characters
Average Response Length: 800-1200 characters

By Source:
- Mushroom cultivation: ~40%
- Pharmaceutical base: ~20%
- ChEMBL targets: ~25%
- Hugging Face integration: ~10%
- Hybrid examples: ~5%

By Category:
- Drug targets: ~30%
- Cultivation expertise: ~25%
- Pharmacology: ~15%
- Medicinal chemistry: ~10%
- Machine learning: ~10%
- Others: ~10%
```

---

## Model Building

### Build Local Model with Ollama

```bash
# 1. Create the model from Modelfile
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile

# 2. Verify model creation
ollama list

# 3. Test the model
ollama run CroweLogic-Pharma:latest
```

### Interactive Testing

```bash
# Start interactive session
ollama run CroweLogic-Pharma:latest

# Test queries:
>>> What are the therapeutic applications of ganoderic acids from Reishi?
>>> How do I interpret IC50 values in drug discovery?
>>> Design a ChEMBL-based workflow for target identification.
>>> What is the SMILES notation for aspirin?
```

### Programmatic API Usage

```python
import requests
import json

def query_model(prompt):
    response = requests.post('http://localhost:11434/api/generate',
        json={
            "model": "CroweLogic-Pharma:latest",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()['response']

# Example
answer = query_model("How do you use ChEMBL for SAR analysis?")
print(answer)
```

---

## Azure Deployment

### Quick Deployment to Azure Container Instances

```bash
# 1. Create deployment configuration
python azure_deployment/deploy_azure.py --config

# 2. Edit deployment_config.json
# Update with your Azure subscription details

# 3. Deploy to Azure
python azure_deployment/deploy_azure.py --type aci
```

### Deployment Process

The script will:
1. ✓ Check Azure CLI installation
2. ✓ Login to Azure account
3. ✓ Create resource group
4. ✓ Create Azure Container Registry
5. ✓ Build Docker image with model
6. ✓ Push image to ACR
7. ✓ Deploy container to ACI
8. ✓ Provide endpoint URLs

### Post-Deployment

After successful deployment, you'll receive:

```
=== Deployment Complete ===
Endpoint: http://crowelogic-pharma.eastus.azurecontainer.io:11434
API Endpoint: http://crowelogic-pharma.eastus.azurecontainer.io:8000

Access your model:
curl -X POST http://<endpoint>:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "CroweLogic-Pharma", "prompt": "Your question here"}'
```

### Azure Machine Learning Deployment

For production ML workloads:

```bash
# Deploy to Azure ML
python azure_deployment/deploy_azure.py --type azureml

# This creates:
# - Azure ML Workspace
# - Compute environment
# - Model registry entry
# - Managed endpoints (optional)
```

---

## API Usage

### REST API Endpoints

#### Generate Response
```bash
POST /api/generate
{
  "model": "CroweLogic-Pharma",
  "prompt": "What are hericenones?",
  "stream": false
}
```

#### Chat (Multi-turn)
```bash
POST /api/chat
{
  "model": "CroweLogic-Pharma",
  "messages": [
    {"role": "user", "content": "Tell me about Lion's Mane"},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "What are its bioactive compounds?"}
  ]
}
```

#### Generate Embeddings
```bash
POST /api/embeddings
{
  "model": "CroweLogic-Pharma",
  "prompt": "hericenone erinacine neuroprotection"
}
```

### Python SDK

```python
import ollama

# Single query
response = ollama.generate(
    model='CroweLogic-Pharma:latest',
    prompt='Explain QSAR modeling for drug discovery'
)
print(response['response'])

# Streaming response
for chunk in ollama.generate(
    model='CroweLogic-Pharma:latest',
    prompt='Design a screening pipeline for ganoderic acids',
    stream=True
):
    print(chunk['response'], end='', flush=True)

# Chat mode
messages = [
    {'role': 'user', 'content': 'What is ChEMBL?'},
]

response = ollama.chat(
    model='CroweLogic-Pharma:latest',
    messages=messages
)
print(response['message']['content'])
```

### JavaScript/TypeScript

```javascript
const axios = require('axios');

async function queryModel(prompt) {
  const response = await axios.post('http://localhost:11434/api/generate', {
    model: 'CroweLogic-Pharma:latest',
    prompt: prompt,
    stream: false
  });

  return response.data.response;
}

// Usage
queryModel('How do protein-ligand binding assays work?')
  .then(answer => console.log(answer));
```

---

## Monitoring and Maintenance

### Local Monitoring

```bash
# View model info
ollama show CroweLogic-Pharma:latest

# Monitor resource usage
docker stats

# View logs
ollama logs
```

### Azure Monitoring

```bash
# View container logs
az container logs \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --follow

# View metrics
az monitor metrics list \
  --resource <container-resource-id> \
  --metric-names CPUUsage,MemoryUsage
```

### Performance Optimization

**For Local Deployment:**
- Use GPU acceleration if available
- Increase model context window
- Adjust temperature and top-p parameters
- Use quantized models for faster inference

**For Azure Deployment:**
- Enable auto-scaling based on requests
- Use Azure Front Door for load balancing
- Implement caching for common queries
- Monitor costs and optimize compute resources

---

## Updating the Model

### Add New Training Data

```bash
# 1. Add new examples to training_data/custom_examples.jsonl
# 2. Run consolidation
python scripts/consolidate_training_data.py

# 3. Rebuild model
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile --force

# 4. Test updates
ollama run CroweLogic-Pharma:latest
```

### Update Azure Deployment

```bash
# 1. Rebuild and push new image
az acr build \
  --registry crowelogicpharmaacr \
  --image crowelogic-pharma:latest \
  --file azure_deployment/Dockerfile \
  .

# 2. Restart container
az container restart \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci
```

---

## Troubleshooting

### Model Not Responding

**Issue**: Model takes too long or doesn't respond

**Solutions**:
1. Check if Ollama service is running: `ollama serve`
2. Verify model is loaded: `ollama list`
3. Increase timeout in API calls
4. Check system resources (RAM, CPU)

### Azure Deployment Fails

**Issue**: Container fails to start on Azure

**Solutions**:
1. Check logs: `az container logs --resource-group <rg> --name <name>`
2. Verify image exists in ACR
3. Check resource quotas in subscription
4. Ensure Dockerfile builds successfully locally

### Poor Model Performance

**Issue**: Model gives inconsistent or incorrect answers

**Solutions**:
1. Review training data quality
2. Add more domain-specific examples
3. Adjust model parameters (temperature, context window)
4. Verify model loaded correct training data

---

## Cost Optimization

### Azure Cost Estimates

**Container Instances (4 CPU, 16GB RAM)**:
- Continuous: ~$200-300/month
- On-demand (8hrs/day): ~$80-100/month

**Optimization Strategies**:
1. Use Azure Functions for sporadic use
2. Implement auto-shutdown during off-hours
3. Use spot instances for non-critical workloads
4. Consider Azure Kubernetes Service for scale

---

## Support and Resources

### Documentation
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Azure Container Instances](https://docs.microsoft.com/azure/container-instances/)
- [ChEMBL Database](https://www.ebi.ac.uk/chembl/)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)

### Datasets Used
- `alimotahharynia/approved_drug_target` - Approved drug-target pairs
- `antoinebcx/smiles-molecules-chembl` - ChEMBL SMILES data
- `SandboxAQ/SAIR` - Protein-ligand complexes
- `microsoft/BiomedParseData` - Biomedical imaging data

---

**Version**: 2.0.0
**Last Updated**: 2025-11-06
**License**: Private and Confidential
