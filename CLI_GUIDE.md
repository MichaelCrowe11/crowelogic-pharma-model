# CroweLogic-Pharma CLI Guide

Production-ready command-line interface for AI-powered pharmaceutical research with quantum computing integration.

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/michaelcrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Install in development mode
pip install -e .

# Verify installation
crowelogic --version
```

### From PyPI (when published)

```bash
pip install crowelogic-pharma
```

## Quick Start

```bash
# Show system information
crowelogic info

# List available models
crowelogic model list

# Run quantum analysis
crowelogic quantum analyze hericenone_A

# Chat with AI model
crowelogic model chat
```

---

## Commands Overview

### 1. Model Management (`model`)

Manage Ollama AI models for pharmaceutical research.

#### `model list`
List all available Ollama models

```bash
crowelogic model list
```

#### `model chat`
Interactive chat with the pharmaceutical AI

```bash
# Use default model (CroweLogic-Pharma:mini)
crowelogic model chat

# Use specific model
crowelogic model chat --model CroweLogic-Pharma:pro

# One-shot question
crowelogic model chat "What are the therapeutic applications of hericenones?"
```

**Example Session:**
```
╔════════════════════════════════════════════════════════════╗
║  CroweLogic-Pharma Chat (CroweLogic-Pharma:mini)         ║
╚════════════════════════════════════════════════════════════╝

You: Explain the mechanism of action of ganoderic acids
AI:  Ganoderic acids from Reishi mushrooms...

You: exit
```

#### `model create`
Create a new Ollama model from Modelfile

```bash
# Create mini model (1B params)
crowelogic model create --variant mini

# Create standard model (3B params)
crowelogic model create --variant standard

# Create pro model (8B params - requires 16GB RAM)
crowelogic model create --variant pro

# Custom Modelfile
crowelogic model create --modelfile path/to/custom/Modelfile --name MyCustomModel
```

---

### 2. Quantum Chemistry (`quantum`)

Perform quantum mechanical calculations on pharmaceutical compounds.

#### `quantum analyze`
Analyze molecular structure using quantum chemistry

```bash
# Analyze pre-defined compounds
crowelogic quantum analyze hericenone_A
crowelogic quantum analyze ganoderic_acid_A

# Example output:
# ┌───────────────────┬────────────┐
# │ HOMO-LUMO Gap     │ 27.211 eV  │
# │ UV λmax           │ 350.0 nm   │
# │ Reactivity        │ Electr... │
# └───────────────────┴────────────┘
```

**Supported Compounds:**
- `hericenone_A` - Lion's Mane bioactive
- `ganoderic_acid_A` - Reishi bioactive

#### `quantum dock`
Simulate molecular docking with target proteins

```bash
# Dock pre-defined compounds
crowelogic quantum dock hericenone_A
crowelogic quantum dock ganoderic_acid_A

# Example output:
# Target: TrkA (NGF Receptor)
# Docking Score: -6.18 kcal/mol
# Predicted Ki: 12.1 μM
# Drug-likeness: Good
```

---

### 3. Training Data (`data`)

Manage training datasets for model fine-tuning.

#### `data generate`
Generate expanded training data from multiple sources

```bash
# Generate all datasets
crowelogic data generate

# Generate specific source
crowelogic data generate --source huggingface
crowelogic data generate --source chembl
crowelogic data generate --source mushroom

# Specify sample size
crowelogic data generate --samples 500
```

**Data Sources:**
- **HuggingFace**: Drug-target pairs, SMILES molecules, protein-ligand complexes
- **ChEMBL**: Drug targets with bioactivity data
- **Mushroom**: Curated mycopharmacology expert examples

#### `data stats`
Show training data statistics

```bash
crowelogic data stats

# Example output:
# ┌─────────────────┬─────────┐
# │ Total Examples  │ 300+    │
# │ Pharma Base     │ 8       │
# │ Mushroom Expert │ 90      │
# │ ChEMBL Targets  │ 200     │
# └─────────────────┴─────────┘
```

---

### 4. Azure Deployment (`deploy`)

Deploy models to Azure cloud infrastructure.

#### `deploy config`
Configure Azure deployment settings

```bash
crowelogic deploy config

# Interactive prompts will ask for:
# - Azure Subscription ID
# - Resource Group Name
# - Location (eastus, westus, etc.)
# - Container Registry Name
# - Compute Configuration
```

**Configuration saved to:** `azure_deployment/deployment_config.json`

#### `deploy start`
Deploy to Azure

```bash
# Deploy to Azure Container Instances (recommended)
crowelogic deploy start --type aci

# Deploy to Azure ML
crowelogic deploy start --type azureml

# Deployment steps:
# 1. ✓ Login to Azure
# 2. ✓ Create Resource Group
# 3. ✓ Create Container Registry
# 4. ✓ Build and push Docker image
# 5. ✓ Deploy container
# 6. ✓ Get endpoint URL
```

**Azure Resources Created:**
- Resource Group: `crowelogic-pharma-rg`
- Container Registry: `crowelogicpharmaacr`
- Container Instance: `crowelogic-pharma-aci`
- Public Endpoint: `http://<ip>:11434/api/generate`

---

### 5. Configuration (`cfg`)

Manage CLI configuration settings.

#### `cfg show`
Display current configuration

```bash
crowelogic cfg show

# Example output:
# ┌──────────────────┬──────────────────────────┐
# │ default_model    │ CroweLogic-Pharma:mini   │
# │ azure_enabled    │ False                    │
# └──────────────────┴──────────────────────────┘
```

#### `cfg set`
Set configuration value

```bash
# Set default model
crowelogic cfg set default_model CroweLogic-Pharma:pro

# Enable Azure integration
crowelogic cfg set azure_enabled true
```

#### `cfg reset`
Reset configuration to defaults

```bash
crowelogic cfg reset
```

**Config File Location:** `~/.crowelogic-pharma/config.json`

---

### 6. System Information (`info`)

Display system and environment information.

```bash
crowelogic info
```

**Shows:**
- CLI version
- Python version
- Platform (OS)
- Ollama status
- Synapse-Lang availability
- Azure CLI status
- Config file location
- Default model

---

### 7. Demonstrations (`demo`)

Run pre-built demonstration scripts.

```bash
# Full integrated pipeline (quantum + docking + AI)
crowelogic demo full

# Quantum chemistry only
crowelogic demo quantum

# Molecular docking only
crowelogic demo docking
```

**Demo Output:**
```
==================================================================
SYNAPSE-PHARMA INTEGRATED DRUG DISCOVERY AI
Quantum Computing + AI-Driven Pharmaceutical Research
==================================================================

COMPOUND 1: HERICENONE A (Hericium erinaceus - Lion's Mane)

🔬 [STEP 1: QUANTUM CHEMISTRY ANALYSIS]
   HOMO-LUMO Gap:        27.211 eV
   UV λmax:              350.0 nm
   Reactivity:           Electrophilic
   Aromaticity:          High

🎯 [STEP 2: MOLECULAR DOCKING]
   Target Protein:       TrkA (NGF Receptor)
   Docking Score:        -6.18 kcal/mol
   Predicted Ki:         12.1 μM

💊 [STEP 3: ADME-TOX PREDICTION]
   Drug-likeness:        Good
   Oral Bioavailability: ✓ YES
   BBB Penetration:      ✓ YES

🤖 [STEP 4: AI RECOMMENDATION]
   Development Potential: Good
   Clinical Applications: Neuroprotection, cognitive enhancement
```

---

## Configuration File

The CLI stores configuration in JSON format at `~/.crowelogic-pharma/config.json`:

```json
{
  "default_model": "CroweLogic-Pharma:mini",
  "azure_enabled": false,
  "azure_subscription_id": "",
  "azure_resource_group": "crowelogic-pharma-rg",
  "data_sources": {
    "huggingface": true,
    "chembl": true,
    "mushroom": true
  },
  "quantum_compute": {
    "method": "huckel",
    "basis_set": "sto-3g"
  }
}
```

---

## Common Workflows

### Workflow 1: Analyze New Compound

```bash
# 1. Run quantum analysis
crowelogic quantum analyze hericenone_A

# 2. Run docking simulation
crowelogic quantum dock hericenone_A

# 3. Get AI interpretation
crowelogic model chat "Interpret these results for clinical development"
```

### Workflow 2: Model Development & Deployment

```bash
# 1. Generate training data
crowelogic data generate --samples 500

# 2. Create optimized model
crowelogic model create --variant standard

# 3. Test locally
crowelogic model chat

# 4. Configure Azure
crowelogic deploy config

# 5. Deploy to cloud
crowelogic deploy start --type aci
```

### Workflow 3: Research Analysis

```bash
# 1. Check system readiness
crowelogic info

# 2. Run full demo to understand capabilities
crowelogic demo full

# 3. Analyze specific compound
crowelogic quantum analyze hericenone_A

# 4. Interactive research session
crowelogic model chat --model CroweLogic-Pharma:pro
```

---

## Environment Variables

```bash
# Ollama server URL (default: http://localhost:11434)
export OLLAMA_HOST=http://localhost:11434

# Azure subscription ID
export AZURE_SUBSCRIPTION_ID=your-subscription-id

# Enable debug mode
export CROWELOGIC_DEBUG=1
```

---

## Troubleshooting

### Ollama Not Found

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve
```

### Azure CLI Not Found

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login
```

### Model Not Available

```bash
# Create the model
crowelogic model create --variant mini

# Or pull from Ollama registry
ollama pull llama3.2:1b
```

### Synapse-Lang Import Error

```bash
# Install quantum computing dependencies
pip install synapse-lang numba
```

---

## Advanced Usage

### Custom Modelfile

Create custom model with specific parameters:

```dockerfile
# custom_modelfile
FROM llama3.2:3b

PARAMETER temperature 0.7
PARAMETER top_p 0.9

SYSTEM """
You are a pharmaceutical research assistant specializing in...
"""
```

```bash
crowelogic model create --modelfile custom_modelfile --name MyCustomPharmaAI
```

### Batch Analysis

Analyze multiple compounds programmatically:

```bash
for compound in hericenone_A ganoderic_acid_A; do
  crowelogic quantum analyze $compound >> results.txt
done
```

### Azure Production Deployment

```bash
# Configure for production
crowelogic cfg set default_model CroweLogic-Pharma:pro
crowelogic cfg set azure_enabled true

# Deploy with GPU support
# Edit Dockerfile to use Dockerfile-gpu
crowelogic deploy start --type azureml --gpu-count 1
```

---

## API Integration

The CLI can be used alongside the Python API:

```python
from synapse_pharma_integration import DrugDiscoveryAI
import subprocess

# Use Python API
ai = DrugDiscoveryAI()
results = ai.full_analysis('hericenone_A')

# Use CLI via subprocess
subprocess.run(['crowelogic', 'quantum', 'analyze', 'hericenone_A'])

# Query Ollama model
subprocess.run(['crowelogic', 'model', 'chat', 'your question here'])
```

---

## Contributing

### Development Setup

```bash
git clone https://github.com/michaelcrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Install in editable mode with dev dependencies
pip install -e .[dev]

# Run tests
pytest tests/

# Format code
black crowelogic_pharma_cli.py

# Lint
flake8 crowelogic_pharma_cli.py
```

---

## Support

- **GitHub Issues**: https://github.com/michaelcrowe11/crowelogic-pharma-model/issues
- **Documentation**: https://github.com/michaelcrowe11/crowelogic-pharma-model
- **Email**: michael@crowelogic.com

---

## Version History

### v3.0.0 (2025-11-06)
- Production-ready CLI with Click/Rich framework
- Azure deployment integration
- Quantum chemistry engine (Synapse-Lang)
- Expanded training data (300+ examples)
- Model variants (mini/standard/pro/enterprise)

### v2.0.0 (Earlier)
- ChEMBL integration (200+ targets)
- HuggingFace dataset integration
- Azure ML deployment scripts

### v1.0.0 (Initial)
- Base pharmaceutical AI model
- Mushroom cultivation expertise
- Ollama integration

---

**Built with 🍄 for advancing mushroom-derived therapeutics**
