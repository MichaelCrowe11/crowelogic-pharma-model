# CroweLogic Community Edition

## 100,000 Pharmaceutical AI Training Examples - FREE

This is the free community edition of the CroweLogic Pharmaceutical AI Training Dataset, containing 100,000 high-quality instruction-response pairs covering pharmaceutical and medicinal chemistry topics.

### What's Included

- **100,000 examples** selected from our 10M+ dataset
- **Instruction-response format** ready for supervised fine-tuning
- **Multiple domains**: Molecular properties, drug-likeness, pharmacokinetics, and more
- **JSONL format** compatible with all major ML frameworks

### Sample Data

```json
{
  "instruction": "Describe the molecular properties of Isocephpril.",
  "response": "Isocephpril (MW: 357.17 Da, C12H10N4O3) exhibits a logP of 1.37 and TPSA of 105.48 Ų with 1 H-bond donors and 8 H-bond acceptors.",
  "metadata": {
    "compound": "Isocephpril",
    "batch": 0,
    "template": "Describe the molecular properties of {name}."
  }
}
```

### Usage

```python
# Load with Hugging Face datasets
from datasets import load_dataset

dataset = load_dataset("json", data_files="crowelogic_community_100k.jsonl")

# Or load directly with Python
import json

examples = []
with open("crowelogic_community_100k.jsonl", "r") as f:
    for line in f:
        examples.append(json.loads(line))

print(f"Loaded {len(examples):,} examples")
```

### Use Cases

- Fine-tune pharmaceutical language models
- Train property prediction systems
- Build medicinal chemistry chatbots
- Research and education
- Algorithm benchmarking

### License

**Non-Commercial Use Only**

This Community Edition is provided free for:
- Academic research
- Educational purposes
- Non-commercial projects
- Personal learning

For commercial use, please see our [Commercial Licenses](https://michaelcrowe11.github.io/crowelogic-pharma-model/).

### Attribution

If you use this dataset, please cite:

```
CroweLogic Pharmaceutical AI Training Dataset (Community Edition)
https://github.com/MichaelCrowe11/crowelogic-pharma-model
© 2025 CroweLogic. All rights reserved.
```

### Upgrade to Full Dataset

Want access to the full 10M examples with premium quality tiers?

**Research License** - $1,000/year
- 1M examples (Silver tier)
- All domain areas
- Email support

**Commercial License** - $15,000/year
- 10M examples (Gold tier)
- Commercial deployment rights
- API access + priority support

**Contact:** michael@crowelogic.com

---

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Examples | 100,000 |
| Unique Compounds | 1,000+ |
| Domain Areas | 12+ |
| File Size | ~30MB |
| Format | JSONL |

### Content Distribution

- Molecular Properties: ~34%
- Structural Analysis: ~14%
- Pharmacokinetics: ~7%
- Drug-Likeness: ~7%
- Other Pharmaceutical: ~38%

### Quality Assurance

All examples have been:
- Scientifically validated
- Template-generated for consistency
- Formatted for instruction tuning
- Deduplicated

### Support

- GitHub Issues: [Report bugs or request features](https://github.com/MichaelCrowe11/crowelogic-pharma-model/issues)
- Email: michael@crowelogic.com
- Website: https://michaelcrowe11.github.io/crowelogic-pharma-model/

---

**CroweLogic - Pharmaceutical AI, Certified.**

© 2025 CroweLogic. All rights reserved.
