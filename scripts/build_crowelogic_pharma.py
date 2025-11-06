#!/usr/bin/env python3
"""
CroweLogic-Pharma Training Data Builder
Consolidates mushroom cultivation, pharmaceutical, and biomedical knowledge
"""

import json
import csv
import os
from pathlib import Path

class CroweLogicPharmaBuilder:
    def __init__(self):
        self.training_data = []

    def load_mushroom_knowledge(self, file_path):
        """Load mushroom cultivation knowledge database"""
        print(f"Loading mushroom knowledge from {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract cultivation parameters and create training examples
        if 'temperature' in data:
            for entry in data['temperature'][:20]:  # Sample first 20
                prompt = f"What temperature is used for {entry.get('video', 'mushroom cultivation')} process?"
                response = f"In the {entry.get('video', 'cultivation')} process, the temperature is approximately {entry['value']} degrees. Context: {entry.get('context', '')[:200]}"
                self.training_data.append({
                    "prompt": prompt,
                    "response": response,
                    "source": "mushroom_knowledge_db",
                    "category": "cultivation_parameters"
                })
        print(f"  Added {len(self.training_data)} cultivation parameter examples")

    def load_expert_training(self, file_path):
        """Load expert mushroom cultivation training data"""
        print(f"Loading expert training data from {file_path}...")
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if 'messages' in entry:
                        messages = entry['messages']
                        user_msg = next((m['content'] for m in messages if m['role'] == 'user'), None)
                        asst_msg = next((m['content'] for m in messages if m['role'] == 'assistant'), None)

                        if user_msg and asst_msg and len(asst_msg) > 100:
                            self.training_data.append({
                                "prompt": user_msg,
                                "response": asst_msg[:500],  # Limit response length
                                "source": "crowelm_expert",
                                "category": "cultivation_expertise"
                            })
                            count += 1
                            if count >= 50:  # Limit to 50 examples
                                break
        print(f"  Added {count} expert cultivation examples")

    def load_csv_training(self, file_path):
        """Load CSV training data"""
        print(f"Loading CSV training data from {file_path}...")
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'prompt' in row and 'completion' in row:
                    self.training_data.append({
                        "prompt": row['prompt'],
                        "response": row['completion'],
                        "source": "mushroom_training_csv",
                        "category": "cultivation_qa"
                    })
                    count += 1
        print(f"  Added {count} CSV Q&A examples")

    def load_pharma_training(self, file_path):
        """Load pharmaceutical domain training data"""
        print(f"Loading pharmaceutical training data from {file_path}...")
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if 'prompt' in entry and 'response' in entry:
                        self.training_data.append({
                            "prompt": entry['prompt'],
                            "response": entry['response'],
                            "source": "pharma_training",
                            "category": "pharmaceutical_expertise"
                        })
                        count += 1
        print(f"  Added {count} pharmaceutical expertise examples")

    def create_hybrid_examples(self):
        """Create hybrid examples connecting mushroom compounds to pharmaceutical applications"""
        print("Creating hybrid mushroom-pharma examples...")

        hybrid_examples = [
            {
                "prompt": "How do cultivation parameters affect the bioactive compound content in Lion's Mane?",
                "response": "Cultivation parameters significantly impact bioactive compound production in Lion's Mane (Hericium erinaceus). Key factors:\n\n1. **Temperature (60-70°F optimal)**: Lower temperatures (60-65°F) increase hericenone and erinacine production by stressing the mycelium slightly, triggering secondary metabolite synthesis.\n\n2. **CO2 Levels**: Elevated CO2 (1000-2000 ppm) during fruiting increases erinacine content by up to 40%.\n\n3. **Substrate Composition**: Supplemented hardwood sawdust with 20% wheat bran optimizes both yield and bioactive content. Oak produces higher erinacine levels than maple.\n\n4. **Light Exposure**: Blue light spectrum (450-470nm) for 12h/day increases hericenone synthesis.\n\n5. **Harvest Timing**: Peak erinacine A content occurs at 70-80% maturity (spines 0.5-0.8 inches).\n\n**Pharmaceutical Relevance:**\nFor medicinal extract production, controlled cultivation optimizes NGF-inducing compounds. Commercial pharmaceutical-grade Lion's Mane requires standardized cultivation with measured bioactive profiles (≥0.5% erinacines by dry weight).",
                "source": "hybrid_synthesis",
                "category": "mushroom_pharma_integration"
            },
            {
                "prompt": "What's the relationship between mushroom contamination control and pharmaceutical manufacturing standards?",
                "response": "Mushroom cultivation contamination control parallels pharmaceutical GMP (Good Manufacturing Practices) in several ways:\n\n**Shared Principles:**\n\n1. **Sterile Technique**: Autoclave sterilization at 121°C/15 PSI = pharmaceutical terminal sterilization standards\n2. **Environmental Monitoring**: HEPA-filtered grow rooms (99.97% at 0.3μm) = pharmaceutical cleanroom Class 10,000\n3. **Quality Control**: Testing for contamination = pharmaceutical microbial limits testing\n4. **Traceability**: Batch tracking in mushroom cultivation = pharmaceutical lot genealogy\n\n**Pharmaceutical Translation:**\nFor medicinal mushroom extracts destined for pharmaceutical use:\n- Cultivation must meet GMP standards\n- Documented sterilization cycles with biological indicators\n- Environmental monitoring (particle counts, microbial air sampling)\n- Contamination limits: <100 CFU/g total aerobic count, <10 CFU/g yeast/mold\n- Heavy metal testing (Pb, Cd, Hg, As)\n- Pesticide residue screening\n\n**Key Difference:**\nMushroooms grow contaminants (visible mold), while pharmaceuticals test for them. But both require validated sterile processing and environmental control to ensure product safety and efficacy.\n\nCommercial medicinal mushroom producers seeking pharmaceutical markets must upgrade from basic cultivation contamination control to full GMP compliance.",
                "source": "hybrid_synthesis",
                "category": "mushroom_pharma_integration"
            },
            {
                "prompt": "Design an extraction protocol for isolating hericenones from cultivated Lion's Mane for pharmaceutical applications.",
                "response": "Pharmaceutical-grade hericenone extraction protocol:\n\n**Starting Material:**\n- Fresh Lion's Mane fruiting bodies, harvested at 70-80% maturity\n- GMP-cultivated with documented parameters\n- Dried at 60°C for 16 hours to 10% moisture\n- Ground to 40-60 mesh particle size\n\n**Extraction Protocol:**\n\n**1. Ethanol Extraction (Hericenones are alcohol-soluble):**\n- Material-to-solvent ratio: 1:10 (w/v)\n- 95% ethanol at room temperature\n- Maceration with stirring for 24 hours\n- Repeat extraction twice\n- Combine extracts and filter through 0.45μm membrane\n\n**2. Concentration:**\n- Rotary evaporation at 45°C under vacuum\n- Concentrate to 20% original volume\n\n**3. Purification:**\n- Liquid-liquid partition: ethyl acetate vs water\n- Hericenones partition to organic phase\n- Silica gel column chromatography\n- Gradient elution: hexane → ethyl acetate → methanol\n\n**4. Analysis & Standardization:**\n- HPLC quantification (UV detection at 280nm)\n- Target: ≥3% total hericenones (A-H)\n- LC-MS confirmation of molecular weights\n- NMR structural verification\n\n**5. Pharmaceutical Formulation:**\n- Dissolve in pharmaceutical-grade ethanol\n- Mix with excipients (microcrystalline cellulose, magnesium stearate)\n- Encapsulate in vegetarian capsules\n- Standardize to defined hericenone content (e.g., 500mg extract = 15mg hericenones)\n\n**Quality Control:**\n- Microbial limits testing\n- Heavy metals screening\n- Pesticide residue analysis\n- Stability testing (ICH guidelines)\n- Dissolution testing\n\n**Yield:**\nExpect 5-8% extract yield from dried mushroom, with 2-4% hericenone content in final extract.\n\n**Regulatory Path:**\nThis process would support IND filing for clinical trials evaluating cognitive benefits in MCI patients.",
                "source": "hybrid_synthesis",
                "category": "mushroom_pharma_integration"
            }
        ]

        self.training_data.extend(hybrid_examples)
        print(f"  Added {len(hybrid_examples)} hybrid examples")

    def build_dataset(self):
        """Build complete CroweLogic-Pharma training dataset"""
        print("\n=== Building CroweLogic-Pharma Training Dataset ===\n")

        # Load all data sources
        if os.path.exists("mushroom_knowledge_database.json"):
            self.load_mushroom_knowledge("mushroom_knowledge_database.json")

        if os.path.exists("crowelm_expert_training_data.jsonl"):
            self.load_expert_training("crowelm_expert_training_data.jsonl")

        if os.path.exists("mushroom_training_data.csv"):
            self.load_csv_training("mushroom_training_data.csv")

        if os.path.exists("crowelogic_pharma_training.jsonl"):
            self.load_pharma_training("crowelogic_pharma_training.jsonl")

        # Create hybrid examples
        self.create_hybrid_examples()

        print(f"\n=== Dataset Summary ===")
        print(f"Total training examples: {len(self.training_data)}")

        # Category breakdown
        categories = {}
        for example in self.training_data:
            cat = example.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        print("\nExamples by category:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        return self.training_data

    def save_training_data(self, output_file="crowelogic_pharma_complete_training.jsonl"):
        """Save consolidated training data"""
        print(f"\nSaving training data to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for example in self.training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        print(f"  Saved {len(self.training_data)} examples")

        # Also create Ollama-compatible format
        ollama_file = output_file.replace('.jsonl', '_ollama.jsonl')
        print(f"\nCreating Ollama-compatible format: {ollama_file}...")
        with open(ollama_file, 'w', encoding='utf-8') as f:
            for example in self.training_data:
                ollama_format = {
                    "prompt": example['prompt'],
                    "response": example['response']
                }
                f.write(json.dumps(ollama_format, ensure_ascii=False) + '\n')
        print(f"  Saved Ollama format")

        return output_file, ollama_file

def main():
    builder = CroweLogicPharmaBuilder()
    builder.build_dataset()
    training_file, ollama_file = builder.save_training_data()

    print("\n=== Next Steps ===")
    print(f"1. Training data created: {training_file}")
    print(f"2. Ollama format: {ollama_file}")
    print(f"3. Build model with: ollama create CroweLogic-Pharma:120b-v2 -f CroweLogicPharmaModelfile")
    print(f"4. Test with: ollama run CroweLogic-Pharma:120b-v2")
    print("\n✓ Training data preparation complete!")

if __name__ == "__main__":
    main()
