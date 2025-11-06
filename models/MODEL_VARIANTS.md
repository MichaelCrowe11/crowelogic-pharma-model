# CroweLogic-Pharma Model Variants

Different versions of the CroweLogic-Pharma model optimized for various use cases and hardware requirements.

## Quick Comparison

| Variant | Base Model | Size | RAM Required | Speed | Best For |
|---------|-----------|------|--------------|-------|----------|
| **Mini** | llama3.2:1b | ~700MB | 2GB | Very Fast | Testing, Development, Codespaces |
| **Standard** | llama3.2:3b | ~2GB | 4-8GB | Fast | Daily use, Local machines |
| **Pro** | llama3.1:8b | ~4.7GB | 8-16GB | Medium | Production, Detailed analysis |
| **Enterprise** | llama3.1:70b | ~40GB | 64GB+ | Slow | Research clusters, Maximum quality |
| **Original** | gpt-oss:120b | ~120GB | 128GB+ | Very Slow | High-end servers only |

---

## 1. Mini (Recommended for Codespaces)

**File**: `CroweLogicPharmaModelfile-mini`

### Specs
- **Base Model**: llama3.2:1b
- **Download Size**: ~700MB
- **RAM Required**: 2-4GB
- **Context Window**: 4K tokens
- **Speed**: Very Fast (1-2 sec responses)

### Installation
```bash
ollama pull llama3.2:1b
ollama create CroweLogic-Pharma:mini -f models/CroweLogicPharmaModelfile-mini
ollama run CroweLogic-Pharma:mini
```

### Best For
- ✅ GitHub Codespaces
- ✅ Quick testing and development
- ✅ Low-resource environments
- ✅ Learning and experimentation
- ✅ API prototyping

### Limitations
- Shorter, less detailed responses
- May struggle with very complex queries
- Limited reasoning depth

---

## 2. Standard (Recommended for Most Users)

**File**: `CroweLogicPharmaModelfile-standard`

### Specs
- **Base Model**: llama3.2:3b
- **Download Size**: ~2GB
- **RAM Required**: 4-8GB
- **Context Window**: 8K tokens
- **Speed**: Fast (2-4 sec responses)

### Installation
```bash
ollama pull llama3.2:3b
ollama create CroweLogic-Pharma:standard -f models/CroweLogicPharmaModelfile-standard
ollama run CroweLogic-Pharma:standard
```

### Best For
- ✅ Local development machines
- ✅ Daily pharmaceutical research queries
- ✅ Balanced performance and quality
- ✅ Most production use cases
- ✅ Docker deployments

### Sweet Spot
This is the **recommended version** for most users - great balance of speed, quality, and resource usage.

---

## 3. Pro (High Quality)

**File**: `CroweLogicPharmaModelfile-pro`

### Specs
- **Base Model**: llama3.1:8b
- **Download Size**: ~4.7GB
- **RAM Required**: 8-16GB
- **Context Window**: 16K tokens
- **Speed**: Medium (3-6 sec responses)

### Installation
```bash
ollama pull llama3.1:8b
ollama create CroweLogic-Pharma:pro -f models/CroweLogicPharmaModelfile-pro
ollama run CroweLogic-Pharma:pro
```

### Best For
- ✅ Detailed pharmaceutical analysis
- ✅ Complex SAR/QSAR queries
- ✅ Multi-step reasoning
- ✅ Production deployments with quality requirements
- ✅ Research applications

---

## 4. Enterprise (Maximum Quality)

**File**: `CroweLogicPharmaModelfile-enterprise`

### Specs
- **Base Model**: llama3.1:70b
- **Download Size**: ~40GB
- **RAM Required**: 64GB+
- **Context Window**: 32K tokens
- **Speed**: Slow (10-30 sec responses)
- **GPU**: Highly recommended (RTX 4090, A100)

### Installation
```bash
ollama pull llama3.1:70b
ollama create CroweLogic-Pharma:enterprise -f models/CroweLogicPharmaModelfile-enterprise
ollama run CroweLogic-Pharma:enterprise
```

### Best For
- ✅ Research institutions
- ✅ Maximum quality requirements
- ✅ Complex drug discovery workflows
- ✅ Multi-step analysis pipelines
- ✅ High-end workstations or servers

### Requirements
- GPU with 48GB+ VRAM (e.g., A100, H100)
- OR 64GB+ RAM for CPU inference (very slow)

---

## 5. Original (120B - Not Recommended)

**File**: `CroweLogicPharmaModelfile` (original)

### Specs
- **Base Model**: gpt-oss:120b-cloud
- **Download Size**: ~120GB
- **RAM Required**: 128GB+
- **Context Window**: 131K tokens
- **Speed**: Very Slow (30-120 sec responses)

### Status
⚠️ **Not available** - The gpt-oss:120b-cloud model is not publicly available through Ollama.

This was the original aspirational configuration but is impractical for most use cases.

---

## Choosing the Right Variant

### Decision Tree

```
Are you in Codespaces or have <4GB RAM?
├─ YES → Use Mini (1B)
└─ NO ↓

Do you need maximum quality and have 64GB+ RAM?
├─ YES → Use Enterprise (70B) or Pro (8B)
└─ NO ↓

Regular use with 4-16GB RAM?
└─ YES → Use Standard (3B) ← RECOMMENDED
```

### By Use Case

| Use Case | Recommended Variant |
|----------|-------------------|
| **Development & Testing** | Mini (1B) |
| **Daily Research Queries** | Standard (3B) |
| **Production API** | Standard (3B) or Pro (8B) |
| **Complex Analysis** | Pro (8B) |
| **Research Institution** | Enterprise (70B) |
| **Codespaces/Cloud IDE** | Mini (1B) |
| **Azure Deployment** | Standard (3B) or Pro (8B) |

### By Hardware

| Your Hardware | Recommended Variant |
|--------------|-------------------|
| **2-4GB RAM** | Mini (1B) |
| **4-8GB RAM** | Standard (3B) |
| **8-16GB RAM** | Standard (3B) or Pro (8B) |
| **16-32GB RAM** | Pro (8B) |
| **32GB+ RAM + GPU** | Enterprise (70B) |

---

## Performance Comparison

Based on typical pharmaceutical queries:

### Response Quality (1-10)
- Mini (1B): 6/10 - Good basics, shorter responses
- Standard (3B): 8/10 - Solid quality, comprehensive
- Pro (8B): 9/10 - Excellent detail and reasoning
- Enterprise (70B): 10/10 - Maximum quality and depth

### Speed (responses per minute)
- Mini (1B): ~30-60 responses/min
- Standard (3B): ~15-30 responses/min
- Pro (8B): ~10-20 responses/min
- Enterprise (70B): ~2-6 responses/min

### Cost (Azure VM)
- Mini (1B): $50-100/month (2 vCPU, 4GB)
- Standard (3B): $100-200/month (4 vCPU, 8GB)
- Pro (8B): $200-400/month (8 vCPU, 16GB)
- Enterprise (70B): $1000-2000/month (GPU VM)

---

## Switching Between Variants

You can have multiple variants installed:

```bash
# Install all variants
ollama create CroweLogic-Pharma:mini -f models/CroweLogicPharmaModelfile-mini
ollama create CroweLogic-Pharma:standard -f models/CroweLogicPharmaModelfile-standard
ollama create CroweLogic-Pharma:pro -f models/CroweLogicPharmaModelfile-pro

# Switch between them
ollama run CroweLogic-Pharma:mini      # Fast testing
ollama run CroweLogic-Pharma:standard  # Daily use
ollama run CroweLogic-Pharma:pro       # Complex queries
```

---

## Recommendations

### For You (in Codespaces):
**Start with Mini**, upgrade to Standard when deploying:
```bash
ollama create CroweLogic-Pharma:mini -f models/CroweLogicPharmaModelfile-mini
```

### For Local Development:
**Use Standard** for best balance:
```bash
ollama create CroweLogic-Pharma:standard -f models/CroweLogicPharmaModelfile-standard
```

### For Azure Deployment:
**Deploy Standard or Pro** depending on budget:
- Standard (3B): Cost-effective, good quality
- Pro (8B): Premium quality, higher cost

---

## Creating Custom Variants

You can create your own variant with different parameters:

```dockerfile
FROM llama3.2:3b  # Choose your base model

PARAMETER temperature 0.05      # Lower = more focused
PARAMETER top_p 0.98            # Nucleus sampling
PARAMETER num_ctx 8192          # Context window size

SYSTEM """Your custom system prompt here"""
```

Then create:
```bash
ollama create CroweLogic-Pharma:custom -f models/YourModelfile
```

---

**Last Updated**: 2025-11-06
**Recommended Default**: Standard (3B)
