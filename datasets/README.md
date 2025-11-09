# Training Datasets

This directory contains the training data for the CroweLogic-Pharma model.

## Dataset Files

Due to file size, the datasets are not stored in this git repository. They can be downloaded from:

- **Hugging Face Dataset:** [MichaelCrowe11/crowelogic-pharma-100k](https://huggingface.co/datasets/MichaelCrowe11/crowelogic-pharma-100k) (coming soon)
- **Direct Download:** Contact repository owner

### Expected Files

```
crowelogic_pharma_100k_train.jsonl    # 95,000 training examples (~32 MB)
crowelogic_pharma_100k_val.jsonl      # 5,000 validation examples (~1.7 MB)
crowelogic_pharma_enhanced.jsonl      # 9,172 base examples (~3 MB)
```

## Dataset Format

Each line in the JSONL files contains a single training example in the following format:

```json
{
  "instruction": "What is the molecular formula of penicillin G?",
  "response": "The molecular formula of penicillin G is C16H18N2O4S. This naturally occurring penicillin..."
}
```

## Dataset Composition

### 100K Dataset (crowelogic_pharma_100k_*.jsonl)

**Total Examples:** 100,000
- Training: 95,000 (95%)
- Validation: 5,000 (5%)

**Content Breakdown:**
```
75,000 examples (75%): Pharmaceutical Knowledge
  - Molecular properties and drug-likeness analysis
  - Mechanisms of action for major drug classes
  - Pharmacokinetics (ADME) and pharmacodynamics
  - Clinical applications and therapeutic uses
  - Adverse effects and contraindications
  - Drug interactions and resistance mechanisms

16,000 examples (16%): Crowe Logic Patterns
  - Multi-phase analysis pipeline architecture
  - Ensemble ML methodologies
  - Fungal intelligence system design
  - Research workflow patterns
  - Breakthrough scoring systems

7,000 examples (7%): Code Implementations
  - TypeScript patterns (Next.js, React)
  - Python scientific computing
  - API design and data modeling
  - State management patterns
  - Authentication and security

2,000 examples (2%): System Design
  - Architecture decision-making
  - Scalability patterns
  - Database design
  - Performance optimization
```

### Enhanced Dataset (crowelogic_pharma_enhanced.jsonl)

**Total Examples:** 9,172
- Original high-quality examples before variation generation
- Can be used for smaller-scale training or fine-tuning experiments

**Content Breakdown:**
```
6,872 examples: Pharmaceutical Knowledge
1,500 examples: Crowe Logic Patterns
600 examples: Code Implementations
200 examples: System Design
```

## Data Quality

All examples follow these quality standards:

1. **Accuracy:** Information verified against PubChem, medical literature, and production code
2. **Clarity:** Instructions are clear and unambiguous
3. **Completeness:** Responses are comprehensive and educational
4. **Formatting:** Consistent Mistral instruction format: `<s>[INST] {instruction} [/INST] {response}</s>`
5. **Diversity:** Wide range of topics, complexity levels, and query types

## Data Sources

### Pharmaceutical Data
- **PubChem:** Molecular properties, SMILES, drug information
- **Synthetic Generation:** Mechanisms, clinical scenarios, pharmacology
- **Medical Literature:** Drug interactions, resistance mechanisms

### Crowe Logic Data
- **CroweLogicAI Repository:** TypeScript/Next.js patterns, API design
- **crowe-ml-pipeline Repository:** Python ML code, data pipelines
- **Architectural Documentation:** System design patterns, methodologies

## Example Training Pairs

### Pharmaceutical Query
```json
{
  "instruction": "Does amoxicillin satisfy Lipinski's Rule of Five?",
  "response": "Analyzing amoxicillin: MW=365.4 (<500), logP=0.9 (<5), H-donors=4 (≤5), H-acceptors=6 (≤10). This compound satisfies Lipinski's Rule of Five with 0 violations, suggesting good oral bioavailability."
}
```

### Crowe Logic Pattern
```json
{
  "instruction": "Explain the Crowe Logic multi-phase analysis pipeline.",
  "response": "The Crowe Logic architecture uses a 6-phase analysis pipeline inspired by fungal lifecycles: (1) Data Collection Layer - substrate identification and ingestion, (2) Spore Analysis - initial data decomposition, (3) Mycelial Network Formation - relationship mapping, (4) Ensemble Learning - Random Forest + Gradient Boosting combination, (5) Breakthrough Scoring - multi-criteria evaluation, (6) Results Synthesis - actionable insights generation."
}
```

### Code Implementation
```json
{
  "instruction": "How do you implement Redis data layer with user namespacing in Next.js?",
  "response": "Use a Redis client with key prefixing pattern: `${userId}:${dataKey}`. Create a data access layer:\n\n```typescript\nimport Redis from 'ioredis';\n\nconst redis = new Redis(process.env.REDIS_URL);\n\nexport async function getUserData(userId: string, key: string) {\n  return redis.get(`user:${userId}:${key}`);\n}\n\nexport async function setUserData(userId: string, key: string, value: string) {\n  return redis.set(`user:${userId}:${key}`, value);\n}\n```\n\nThis ensures data isolation between users and enables efficient key-based queries."
}
```

## Using the Datasets

### Download Datasets

```bash
# Clone repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model
cd crowelogic-pharma-model/datasets

# Download from Hugging Face (requires huggingface-cli)
huggingface-cli download MichaelCrowe11/crowelogic-pharma-100k \
  --repo-type dataset \
  --local-dir .

# Or manually download and place files here
```

### Load in Python

```python
import json

# Load training data
train_data = []
with open('datasets/crowelogic_pharma_100k_train.jsonl', 'r') as f:
    for line in f:
        train_data.append(json.loads(line))

print(f"Loaded {len(train_data)} training examples")
```

### Use with Hugging Face Datasets

```python
from datasets import load_dataset

# Load from local files
dataset = load_dataset('json', data_files={
    'train': 'datasets/crowelogic_pharma_100k_train.jsonl',
    'validation': 'datasets/crowelogic_pharma_100k_val.jsonl'
})

print(dataset)
# DatasetDict({
#     train: Dataset({
#         features: ['instruction', 'response'],
#         num_rows: 95000
#     })
#     validation: Dataset({
#         features: ['instruction', 'response'],
#         num_rows: 5000
#     })
# })
```

## Data Statistics

```
Total unique compounds: 37 pharmaceutical compounds
Total code files analyzed: 50+ TypeScript/Python files
Total patterns extracted: 2,300+ distinct patterns
Average instruction length: ~45 words
Average response length: ~150 words
Token distribution: 200-800 tokens per example
```

## License

The datasets are released under the same MIT License as the model repository.

## Citation

If you use these datasets in your research:

```bibtex
@misc{crowelogic-pharma-dataset-2025,
  author = {Michael Crowe},
  title = {CroweLogic-Pharma Training Dataset},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/MichaelCrowe11/crowelogic-pharma-model}
}
```

## Contact

For questions about the datasets or to request access:
- GitHub: [@MichaelCrowe11](https://github.com/MichaelCrowe11)
- Repository Issues: https://github.com/MichaelCrowe11/crowelogic-pharma-model/issues
