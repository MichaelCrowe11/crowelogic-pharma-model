# CroweLogic-Pharma: AI-Powered Pharmaceutical Research Platform

An advanced AI system specializing in pharmaceutical research, drug discovery, and biomedical innovation, with particular expertise in mycopharmacology and mushroom-derived therapeutics.

## 🔬 Core Capabilities

- **Medicinal Chemistry**: Drug design, SAR analysis, lead optimization
- **Pharmacology**: ADME-Tox prediction, target identification, mechanism of action
- **Biomedical Research**: Disease pathways, therapeutic targets, clinical trial design
- **Cheminformatics**: Molecular property prediction, compound screening, QSAR modeling
- **Mycopharmacology**: Mushroom-derived therapeutics, natural product discovery
- **Computational Drug Discovery**: Molecular docking, virtual screening, binding affinity prediction

## 🍄 Specialized Knowledge

### Mushroom Bioactive Compounds
- **Hericenones & Erinacines** (Lion's Mane): NGF stimulation, neuroprotection
- **Ganoderic Acids** (Reishi): Anti-inflammatory, anticancer, hepatoprotective
- **Beta-glucans**: Immunomodulation, antitumor activity

### Therapeutic Applications
- Neurodegenerative diseases (Alzheimer's, Parkinson's, ALS)
- Oncology and immunotherapy
- Neuroprotection and cognitive enhancement

## 📊 Model Specifications

- **Base Model**: GPT-OSS 120B
- **Parameters**: 116.8B
- **Context Length**: 131,072 tokens
- **Quantization**: MXFP4

## 🚀 Quick Start

### Local Deployment

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Generate expanded training data
python scripts/add_huggingface_data.py
python scripts/consolidate_training_data.py

# 4. Create the model
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile

# 5. Run the model
ollama run CroweLogic-Pharma:latest
```

### Azure Deployment

```bash
# 1. Configure deployment
python azure_deployment/deploy_azure.py --config

# 2. Deploy to Azure Container Instances
python azure_deployment/deploy_azure.py --type aci

# 3. Access via endpoint
curl -X POST http://<your-endpoint>:11434/api/generate \
  -d '{"model": "CroweLogic-Pharma", "prompt": "Your question"}'
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

## 📁 Repository Structure

```
crowelogic-pharma-model/
├── models/                      # Model configurations
│   ├── CroweLogicPharmaModelfile    # Main Ollama Modelfile
│   ├── advanced_modelfile           # Advanced configuration
│   └── quantumchem_modelfile        # Quantum chemistry variant
├── training_data/               # Training datasets
│   ├── pharma_base.jsonl            # Base pharmaceutical knowledge
│   ├── crowelm_expert.jsonl         # Mushroom cultivation expertise
│   ├── huggingface_training_data.jsonl  # HF dataset integration
│   ├── chembl_training_data.jsonl   # ChEMBL drug targets
│   └── crowelogic_pharma_expanded_training.jsonl  # Consolidated dataset
├── scripts/                     # Build and deployment scripts
│   ├── build_crowelogic_pharma.py   # Original build script
│   ├── add_huggingface_data.py      # HuggingFace integration
│   ├── add_chembl_data.py           # Enhanced ChEMBL integration
│   └── consolidate_training_data.py # Data consolidation pipeline
├── azure_deployment/            # Azure deployment files
│   ├── Dockerfile                   # Container configuration
│   ├── deploy_azure.py              # Deployment automation
│   ├── azure-container-instance.yaml # ACI configuration
│   ├── azure-ml-config.yaml         # Azure ML environment
│   └── README.md                    # Deployment guide
├── requirements.txt             # Python dependencies
├── DEPLOYMENT.md                # Complete deployment guide
└── README.md                    # This file
```

## 🎓 Training Data

### Enhanced Dataset (v2.0)

- **Pharmaceutical Domain**: 8 base examples
- **Mushroom Cultivation**: 90+ expert examples
- **ChEMBL Drug Targets**: 200+ target examples with bioactivity interpretation
- **Hugging Face Integrations**: Drug-target pairs, SMILES molecules, protein-ligand complexes
- **Hybrid Knowledge**: 10+ mushroom-pharma integration examples
- **Total**: 300+ curated examples

### Data Sources

1. **Hugging Face Datasets**:
   - `alimotahharynia/approved_drug_target` (1,660 approved drugs, 2,093 targets)
   - `antoinebcx/smiles-molecules-chembl` (ChEMBL SMILES database)
   - `SandboxAQ/SAIR` (1M+ protein-ligand complexes)
   - `microsoft/BiomedParseData` (Biomedical object detection)

2. **ChEMBL Database**:
   - 17,803+ drug targets with GO terms and PDB structures
   - Bioactivity data interpretation (IC50, EC50, Ki, Kd)
   - Structure-activity relationship (SAR) analysis examples

3. **Custom Integration**:
   - Mushroom compound therapeutic validation workflows
   - ML pipelines for natural product drug discovery
   - QSAR modeling for medicinal chemistry

## 🔐 Security & Compliance

- Training data sanitized and validated
- No patient data or proprietary research
- All mushroom data from public educational content
- Pharmaceutical knowledge from published literature

## 📄 License

Private and Confidential - All Rights Reserved

---

**Built with 🍄 for advancing mushroom-derived therapeutics**
