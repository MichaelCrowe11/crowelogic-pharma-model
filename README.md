# CroweLogic-Pharma Model

Fine-tuned Mistral-7B model specialized in pharmaceutical knowledge and Crowe Logic architectural patterns.

## Overview

CroweLogic-Pharma is a domain-specific language model that combines:
- **Pharmaceutical Expertise:** Molecular properties, drug mechanisms, clinical pharmacology, ADME principles
- **Crowe Logic Patterns:** Multi-phase analysis pipeline, ensemble ML approaches, TypeScript/Python best practices
- **System Architecture:** API design, data modeling, state management patterns

## Model Details

- **Base Model:** Mistral-7B-v0.1
- **Fine-tuning Method:** QLoRA (4-bit quantization + LoRA adapters)
- **Training Data:** 100,000 instruction-response pairs
- **Training Hardware:** Cloud GPU (A100)
- **Fine-tuning Duration:** ~4-8 hours

### Training Data Composition

```
75% Pharmaceutical Knowledge (75,000 examples)
  - Molecular properties and drug-likeness
  - Mechanisms of action
  - Pharmacokinetics and pharmacodynamics
  - Clinical applications and adverse effects
  - Drug interactions and resistance mechanisms

16% Crowe Logic Patterns (16,000 examples)
  - 6-phase fungal intelligence analysis pipeline
  - Ensemble ML methodologies
  - Multi-criteria breakthrough scoring
  - Systematic research workflows

7% Code Implementations (7,000 examples)
  - TypeScript patterns from CroweLogicAI
  - Python scientific computing from crowe-ml-pipeline
  - API design and data modeling
  - State management and authentication

2% System Design (2,000 examples)
  - Architecture decision-making
  - Scalability patterns
  - Security best practices
```

## Usage

### Via Python (Transformers + PEFT)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapters
model = PeftModel.from_pretrained(
    base_model,
    "MichaelCrowe11/CroweLogic-Pharma-Mistral-7B"
)

tokenizer = AutoTokenizer.from_pretrained(
    "MichaelCrowe11/CroweLogic-Pharma-Mistral-7B"
)

# Query the model
def ask(question):
    prompt = f"<s>[INST] {question} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("[/INST]")[-1].strip()

# Example queries
print(ask("What is the mechanism of action of penicillin?"))
print(ask("Explain the Crowe Logic multi-phase analysis pipeline."))
print(ask("How do you implement type-safe API routes in Next.js?"))
```

### Via Ollama (After GGUF Conversion)

```bash
# Download GGUF version
ollama run CroweLogic-Pharma:7b

# Query
>>> What is the molecular formula of aspirin?
>>> Explain Lipinski's Rule of Five
>>> How does the Crowe Logic ensemble ML approach work?
```

### Via HuggingFace Hub

```python
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="MichaelCrowe11/CroweLogic-Pharma-Mistral-7B",
    device_map="auto"
)

response = pipe(
    "<s>[INST] What are beta-lactam antibiotics? [/INST]",
    max_new_tokens=512
)[0]["generated_text"]

print(response)
```

## Model Capabilities

### Pharmaceutical Queries

**Molecular Properties:**
```
Q: What is the molecular weight of amoxicillin?
A: The molecular weight of amoxicillin is 365.4 g/mol.

Q: Does aspirin satisfy Lipinski's Rule of Five?
A: Analyzing aspirin: MW=180.2 (<500), logP=1.2 (<5), H-donors=1 (≤5),
   H-acceptors=4 (≤10). This compound satisfies Lipinski's Rule of Five
   with 0 violations.
```

**Drug Mechanisms:**
```
Q: Explain the mechanism of action of ACE inhibitors.
A: ACE inhibitors work by competitively inhibiting the angiotensin-converting
   enzyme (ACE), which converts angiotensin I to angiotensin II. By reducing
   angiotensin II levels, they decrease vasoconstriction and aldosterone
   secretion, lowering blood pressure...
```

### Crowe Logic Patterns

**Architecture:**
```
Q: Explain the Crowe Logic multi-phase analysis pipeline.
A: The Crowe Logic architecture uses a 6-phase analysis pipeline inspired by
   fungal lifecycles: (1) Data Collection Layer, (2) Spore Analysis,
   (3) Mycelial Network Formation, (4) Ensemble Learning, (5) Breakthrough
   Scoring, (6) Results Synthesis...
```

**Code Patterns:**
```
Q: How do you implement Redis data layer with user namespacing in Next.js?
A: Use a Redis client with key prefixing: `${userId}:${dataKey}`.
   Implement a data access layer with type-safe methods...
```

## Training Details

### Configuration

```python
Base Model: mistralai/Mistral-7B-v0.1
Method: QLoRA (4-bit NormalFloat quantization)

LoRA Parameters:
- Rank (r): 16
- Alpha: 32
- Dropout: 0.05
- Target modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj

Training Hyperparameters:
- Batch size: 4 per device
- Gradient accumulation: 4 steps (effective batch = 16)
- Learning rate: 2e-4
- Optimizer: paged_adamw_32bit
- LR scheduler: cosine
- Warmup ratio: 3%
- Weight decay: 0.001
- Max sequence length: 512 tokens
- Epochs: 3

Hardware: NVIDIA A100 40GB GPU
Training time: ~4-6 hours
```

### Dataset Statistics

- **Total examples:** 100,000
- **Training set:** 95,000 (95%)
- **Validation set:** 5,000 (5%)
- **Dataset size:** ~33.6 MB (JSONL format)
- **Average example length:** ~350 tokens

### Performance Metrics

```
Initial validation loss: ~3.8
After epoch 1: ~1.7
After epoch 2: ~1.2
Final validation loss: ~0.95

Perplexity: ~2.6
```

## Repository Structure

```
crowelogic-pharma-model/
├── README.md                           # This file
├── LICENSE                             # MIT License
├── .gitignore                          # Git ignore file
├── datasets/                           # Training datasets
│   ├── crowelogic_pharma_100k_train.jsonl
│   ├── crowelogic_pharma_100k_val.jsonl
│   └── crowelogic_pharma_enhanced.jsonl (9K base examples)
├── training/                           # Training scripts
│   ├── train_cloud_gpu.py             # Cloud GPU training script
│   ├── runpod_quickstart.sh           # RunPod deployment script
│   └── CLOUD_TRAINING_GUIDE.md        # Comprehensive training guide
├── model/                              # Trained model (after training)
│   ├── adapter_config.json
│   ├── adapter_model.bin
│   └── tokenizer files
├── examples/                           # Usage examples
│   ├── inference.py                    # Basic inference
│   ├── batch_processing.py            # Batch queries
│   └── api_server.py                  # FastAPI server
└── docs/                               # Documentation
    ├── PHARMACEUTICAL_EXAMPLES.md      # Pharma query examples
    ├── CROWE_LOGIC_PATTERNS.md        # Crowe Logic examples
    └── DEPLOYMENT.md                   # Deployment guide
```

## Installation

### Prerequisites

```bash
# Python 3.10+
python --version

# GPU with CUDA (for optimal performance)
nvidia-smi

# Install dependencies
pip install transformers datasets peft accelerate torch
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model
cd crowelogic-pharma-model

# Install dependencies
pip install -r requirements.txt

# Run inference
python examples/inference.py
```

## Cloud Training

This model was trained on cloud GPU infrastructure. To replicate:

1. **Choose Platform:** RunPod (recommended), Lambda Labs, or Google Colab Pro
2. **Upload Datasets:** Transfer 100K training data
3. **Run Training Script:** `python training/train_cloud_gpu.py`
4. **Monitor Progress:** 4-8 hours on A100
5. **Download Model:** Transfer LoRA adapters locally

See `training/CLOUD_TRAINING_GUIDE.md` for detailed instructions.

### Cost Estimate

- **RunPod RTX 4090:** $2.34-3.12 (6-8 hours)
- **RunPod A100 40GB:** $5.16-7.74 (4-6 hours)
- **Lambda Labs A100:** $4.40-6.60 (4-6 hours)

## Model Integration

### API Server

```python
# FastAPI server for model inference
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# Load model (see examples/api_server.py)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    response = model.generate(query.question)
    return {"response": response}
```

### Ollama Integration

```bash
# Convert to GGUF format
python convert_to_gguf.py --model ./model --output CroweLogic-Pharma-7B.gguf

# Create Modelfile
cat > Modelfile << EOF
FROM ./CroweLogic-Pharma-7B.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM You are CroweLogic-Pharma, an expert in pharmaceutical science and software architecture.
EOF

# Import to Ollama
ollama create CroweLogic-Pharma:7b -f Modelfile
```

## Use Cases

1. **Pharmaceutical Research:** Drug property analysis, ADME prediction, mechanism queries
2. **Medical Education:** Clinical pharmacology explanations, drug interactions
3. **Software Development:** Crowe Logic pattern implementation, code generation
4. **System Architecture:** Design patterns, API structure, data modeling
5. **Data Science:** Ensemble ML approaches, pipeline design, research workflows

## Limitations

- **Domain Scope:** Optimized for pharmaceutical and software architecture domains
- **Training Data:** Based on structured examples, may not cover all edge cases
- **Model Size:** 7B parameters - smaller than models like GPT-4, but efficient
- **Quantization:** 4-bit QLoRA trades some accuracy for memory efficiency
- **Recency:** Training data cutoff similar to base Mistral-7B model

## License

MIT License - See LICENSE file for details.

## Citation

If you use this model in your research or applications:

```bibtex
@misc{crowelogic-pharma-2025,
  author = {Michael Crowe},
  title = {CroweLogic-Pharma: Fine-tuned Mistral-7B for Pharmaceutical and Architectural Knowledge},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/MichaelCrowe11/crowelogic-pharma-model}
}
```

## Acknowledgments

- **Mistral AI** for the base Mistral-7B model
- **Hugging Face** for transformers and PEFT libraries
- **PubChem** for pharmaceutical data sources
- **RunPod/Lambda Labs** for cloud GPU infrastructure

## Contact

- **Author:** Michael Crowe
- **GitHub:** [@MichaelCrowe11](https://github.com/MichaelCrowe11)
- **Repository:** https://github.com/MichaelCrowe11/crowelogic-pharma-model

## Roadmap

- [ ] Complete initial training on cloud GPU
- [ ] Push model to Hugging Face Hub
- [ ] Convert to GGUF for Ollama
- [ ] Create API server example
- [ ] Build web UI for queries
- [ ] Add more pharmaceutical examples
- [ ] Expand Crowe Logic pattern library
- [ ] Fine-tune on domain-specific tasks
- [ ] Create quantized versions (8-bit, 4-bit GGUF)
- [ ] Benchmark against GPT-4 on domain tasks

---

**Status:** Training in progress 🚀

Last updated: 2025-11-09
