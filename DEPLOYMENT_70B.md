# CroweLogic-Pharma Pro (70b) Deployment Guide

## Overview

CroweLogic-Pharma Pro is the flagship pharmaceutical AI powered by **llama3.1:70b** (70 billion parameters), offering superior reasoning, deeper analysis, and more accurate scientific predictions compared to the standard model.

## Model Comparison

| Feature | Standard (llama3.2) | Pro (llama3.1:70b) |
|---------|--------------------|--------------------|
| **Parameters** | 3B | 70B |
| **Model Size** | 2GB | 40GB |
| **RAM Required** | 16GB | 64GB |
| **CPU Cores** | 4 | 8 |
| **Monthly Cost** | ~$250 | ~$600-700 |
| **Context Window** | 131K tokens | 131K tokens |
| **Response Quality** | Good | Excellent |
| **Complex Reasoning** | Basic | Advanced |
| **Scientific Accuracy** | Standard | High |
| **Multi-step Analysis** | Limited | Strong |
| **Clinical Trial Design** | Basic | Expert-level |
| **Regulatory Knowledge** | General | Detailed |

## When to Use Pro (70b)

### Ideal Use Cases:
- ✅ **Clinical Trial Design**: Phase I-III protocols, endpoint selection, adaptive designs
- ✅ **Regulatory Strategy**: IND/NDA preparation, FDA/EMA submissions
- ✅ **Complex SAR Analysis**: Multi-parameter optimization, pharmacophore modeling
- ✅ **ADME-Tox Prediction**: Detailed metabolism, toxicity assessments
- ✅ **Polypharmacology**: Multi-target analysis, combination strategies
- ✅ **Patent Analysis**: Freedom-to-operate, competitive landscape
- ✅ **Clinical PK/PD**: Dose optimization, biomarker strategies
- ✅ **Risk-Benefit Assessment**: Therapeutic index, safety profiling

### Use Standard Model For:
- Quick literature queries
- Simple mechanism questions
- Basic compound properties
- General pharmaceutical knowledge
- High-volume, simple queries

## Architecture Enhancements

The 70b model includes:

1. **Enhanced System Prompt**:
   - 10 specialized knowledge domains (vs 6 in standard)
   - Advanced analytical capabilities
   - Pharmaceutical calculation support
   - Regulatory and IP considerations

2. **Optimized Parameters**:
   - Lower temperature (0.05) for scientific accuracy
   - Extended context window (131K tokens)
   - Single model loading for memory efficiency

3. **Performance Optimizations**:
   - `OLLAMA_MAX_LOADED_MODELS=1` (prevents OOM)
   - `OLLAMA_NUM_PARALLEL=1` (ensures stability)
   - Optimized batch size for throughput

## Deployment Steps

### Prerequisites
- Azure subscription with sufficient quota (8 CPU, 64GB RAM)
- Docker installed locally
- Azure CLI configured
- jq installed (for JSON parsing)

### Quick Deployment

```bash
# 1. Make script executable
chmod +x deploy_70b.sh

# 2. Run deployment
./deploy_70b.sh
```

The script will:
1. Build optimized Docker image for 70b model
2. Push to Azure Container Registry
3. Deploy to Azure Container Instances
4. Configure environment for optimal performance

**Note**: First startup takes 15-20 minutes to download the 40GB model.

### Manual Deployment

If you prefer manual control:

```bash
# 1. Build and publish Docker image remotely via ACR
az acr build \
  --registry crowelogicpharma60881 \
  --image crowelogic-pharma-pro:latest \
  --file 1211/Dockerfile-70b \
  .

# 2. Get ACR password
ACR_PASSWORD=$(az acr credential show --name crowelogicpharma60881 --query "passwords[0].value" --output tsv)

# 3. Create container instance
az container create \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-pro-aci \
  --image crowelogicpharma60881.azurecr.io/crowelogic-pharma-pro:latest \
  --registry-login-server crowelogicpharma60881.azurecr.io \
  --registry-username crowelogicpharma60881 \
  --registry-password "$ACR_PASSWORD" \
  --dns-name-label crowelogic-pharma-pro \
  --cpu 8 \
  --memory 64 \
  --ports 11434 8000 \
  --ip-address Public \
  --os-type Linux \
  --location eastus \
  --restart-policy Always \
  --environment-variables \
    OLLAMA_HOST=0.0.0.0:11434 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    OLLAMA_NUM_PARALLEL=1
```

## Testing the Deployment

### Basic Test

```bash
curl -X POST http://crowelogic-pharma-pro.eastus.azurecontainer.io:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma-Pro:latest",
    "prompt": "Design a Phase II trial for a novel Alzheimers drug with specific inclusion criteria and endpoints.",
    "stream": false
  }'
```

### Comprehensive Test Suite

```bash
python test_70b_deployment.py http://crowelogic-pharma-pro.eastus.azurecontainer.io:11434
```

### Performance Comparison

```bash
# Compare 70b vs standard model
python test_70b_deployment.py \
  http://crowelogic-pharma-pro.eastus.azurecontainer.io:11434 \
  http://crowelogic-pharma.eastus.azurecontainer.io:11434
```

## Monitoring

### View Logs

```bash
az container logs \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-pro-aci \
  --follow
```

### Check Status

```bash
az container show \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-pro-aci \
  --query "{Name:name,State:instanceView.state,IP:ipAddress.fqdn,CPU:containers[0].resources.requests.cpu,Memory:containers[0].resources.requests.memoryInGb}" \
  --output table
```

### Exec into Container

```bash
az container exec \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-pro-aci \
  --exec-command "/bin/bash"
```

## Cost Management

### Current Costs

- **Pro (70b)**: ~$600-700/month (8 CPU, 64GB RAM)
- **Standard**: ~$250/month (4 CPU, 16GB RAM)

### Cost Optimization Strategies

1. **Stop When Not in Use**
   ```bash
   az container stop --resource-group crowelogic-pharma-rg --name crowelogic-pharma-pro-aci
   az container start --resource-group crowelogic-pharma-rg --name crowelogic-pharma-pro-aci
   ```

2. **Use Standard for Simple Queries**
   - Route simple queries to standard model
   - Reserve 70b for complex analysis

3. **Scheduled Shutdown**
   - Use Azure Automation to stop container during off-hours
   - Startup time with cached model: ~1-2 minutes

## Two-Tier Architecture

For optimal cost-performance, deploy both models:

```
┌─────────────────────────────────────────────────────────────┐
│                    Query Router                              │
│  (Classifies query complexity and routes to appropriate     │
│   model based on required reasoning depth)                   │
└──────────────┬─────────────────────────┬────────────────────┘
               │                         │
               ▼                         ▼
    ┌──────────────────┐     ┌───────────────────────┐
    │  Standard Model  │     │     Pro Model (70b)   │
    │  (llama3.2:3b)   │     │   (llama3.1:70b)      │
    │                  │     │                       │
    │  • Quick queries │     │  • Clinical trials    │
    │  • Simple facts  │     │  • SAR analysis       │
    │  • Literature    │     │  • Regulatory         │
    │  • Basic calcs   │     │  • Multi-target       │
    │                  │     │  • Complex reasoning  │
    │  $250/month      │     │  $600-700/month       │
    └──────────────────┘     └───────────────────────┘
```

## Performance Expectations

### Standard Model (llama3.2)
- Response time: 30-60 seconds for complex queries
- Tokens/second: ~10-15
- Quality: Good for most queries

### Pro Model (llama3.1:70b)
- Response time: 60-120 seconds for complex queries
- Tokens/second: ~5-8
- Quality: Exceptional, research-grade responses

## Troubleshooting

### Container OOM (Out of Memory)
- Ensure `OLLAMA_MAX_LOADED_MODELS=1`
- Verify 64GB RAM allocation
- Check no other models are loaded: `ollama list`

### Slow Performance
- First query after startup is slower (model loading)
- Subsequent queries benefit from caching
- Consider keeping container warm with periodic queries

### Model Not Found
- Model downloads on first startup (15-20 minutes)
- Check logs for download progress
- Verify Ollama service is running

## Next Steps

1. **Deploy the Pro Model**: Run `./deploy_70b.sh`
2. **Test Performance**: Run the test suite
3. **Compare Results**: Use comparison mode to see quality difference
4. **Implement Routing**: Build a query classifier to route between models
5. **Monitor Costs**: Set up Azure cost alerts

---

**Built with 🧬 for advancing pharmaceutical AI research at scale**
