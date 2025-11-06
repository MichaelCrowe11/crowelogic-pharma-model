#!/usr/bin/env python3
"""
Consolidated Training Data Pipeline for CroweLogic-Pharma
Combines all data sources: mushroom knowledge, pharma, ChEMBL, and Hugging Face datasets
"""

import json
import os
from pathlib import Path
from collections import Counter

class TrainingDataConsolidator:
    def __init__(self):
        self.all_training_data = []
        self.stats = {
            'total_examples': 0,
            'by_source': Counter(),
            'by_category': Counter(),
            'avg_prompt_length': 0,
            'avg_response_length': 0
        }

    def load_jsonl_file(self, file_path, source_name):
        """Load training data from JSONL file"""
        if not os.path.exists(file_path):
            print(f"  ⚠ File not found: {file_path}")
            return []

        examples = []
        print(f"  Loading {file_path}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        # Standardize format
                        example = {
                            "prompt": entry.get('prompt', ''),
                            "response": entry.get('response', entry.get('completion', '')),
                            "source": entry.get('source', source_name),
                            "category": entry.get('category', 'general')
                        }

                        if example['prompt'] and example['response']:
                            examples.append(example)
                            self.stats['by_source'][example['source']] += 1
                            self.stats['by_category'][example['category']] += 1
                        else:
                            print(f"    ⚠ Skipping line {line_num}: missing prompt or response")

                    except json.JSONDecodeError as e:
                        print(f"    ⚠ JSON error on line {line_num}: {e}")

        print(f"    Loaded {len(examples)} examples from {source_name}")
        return examples

    def load_existing_training_data(self):
        """Load all existing training data files"""
        print("\n=== Loading Existing Training Data ===\n")

        training_dir = Path("training_data")

        # Load base pharmaceutical training
        pharma_examples = self.load_jsonl_file(
            training_dir / "pharma_base.jsonl",
            "pharma_base"
        )
        self.all_training_data.extend(pharma_examples)

        # Load mushroom expert knowledge
        mushroom_examples = self.load_jsonl_file(
            training_dir / "crowelm_expert.jsonl",
            "mushroom_expert"
        )
        self.all_training_data.extend(mushroom_examples)

        # Load complete training (if exists)
        complete_examples = self.load_jsonl_file(
            training_dir / "crowelogic_pharma_complete_training.jsonl",
            "complete_training"
        )
        # Only add if not duplicate
        existing_prompts = {ex['prompt'] for ex in self.all_training_data}
        new_complete = [ex for ex in complete_examples if ex['prompt'] not in existing_prompts]
        self.all_training_data.extend(new_complete)

        print(f"\n  Total existing examples loaded: {len(self.all_training_data)}")

    def load_new_datasets(self):
        """Load newly generated dataset files"""
        print("\n=== Loading New Dataset Integrations ===\n")

        training_dir = Path("training_data")

        # Load ChEMBL training data
        chembl_examples = self.load_jsonl_file(
            training_dir / "chembl_training_data.jsonl",
            "chembl"
        )
        self.all_training_data.extend(chembl_examples)

        # Load Hugging Face dataset integrations
        hf_examples = self.load_jsonl_file(
            training_dir / "huggingface_training_data.jsonl",
            "huggingface"
        )
        self.all_training_data.extend(hf_examples)

        print(f"\n  Total with new datasets: {len(self.all_training_data)}")

    def deduplicate(self):
        """Remove duplicate examples based on prompt"""
        print("\n=== Deduplicating Training Data ===\n")

        initial_count = len(self.all_training_data)
        seen_prompts = {}
        deduplicated = []

        for example in self.all_training_data:
            prompt = example['prompt'].strip().lower()

            if prompt not in seen_prompts:
                seen_prompts[prompt] = True
                deduplicated.append(example)
            else:
                print(f"  Duplicate found: {example['prompt'][:80]}...")

        self.all_training_data = deduplicated
        duplicates_removed = initial_count - len(deduplicated)

        print(f"\n  Removed {duplicates_removed} duplicates")
        print(f"  Final count: {len(self.all_training_data)} unique examples")

    def validate_quality(self):
        """Validate training data quality"""
        print("\n=== Quality Validation ===\n")

        issues = []

        for i, example in enumerate(self.all_training_data):
            # Check prompt length
            if len(example['prompt']) < 10:
                issues.append(f"Example {i}: Prompt too short")

            # Check response length
            if len(example['response']) < 50:
                issues.append(f"Example {i}: Response too short")

            # Check for required fields
            if not example.get('source'):
                example['source'] = 'unknown'
                issues.append(f"Example {i}: Missing source")

            if not example.get('category'):
                example['category'] = 'general'
                issues.append(f"Example {i}: Missing category")

        if issues:
            print(f"  Found {len(issues)} quality issues:")
            for issue in issues[:10]:  # Show first 10
                print(f"    - {issue}")
            if len(issues) > 10:
                print(f"    ... and {len(issues) - 10} more")
        else:
            print("  ✓ All quality checks passed!")

    def calculate_statistics(self):
        """Calculate dataset statistics"""
        print("\n=== Dataset Statistics ===\n")

        self.stats['total_examples'] = len(self.all_training_data)

        # Calculate average lengths
        prompt_lengths = [len(ex['prompt']) for ex in self.all_training_data]
        response_lengths = [len(ex['response']) for ex in self.all_training_data]

        self.stats['avg_prompt_length'] = sum(prompt_lengths) / len(prompt_lengths) if prompt_lengths else 0
        self.stats['avg_response_length'] = sum(response_lengths) / len(response_lengths) if response_lengths else 0

        print(f"Total Examples: {self.stats['total_examples']}")
        print(f"Average Prompt Length: {self.stats['avg_prompt_length']:.0f} characters")
        print(f"Average Response Length: {self.stats['avg_response_length']:.0f} characters")

        print("\n--- By Source ---")
        for source, count in sorted(self.stats['by_source'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.stats['total_examples']) * 100
            print(f"  {source:30s}: {count:5d} ({percentage:5.1f}%)")

        print("\n--- By Category ---")
        for category, count in sorted(self.stats['by_category'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.stats['total_examples']) * 100
            print(f"  {category:30s}: {count:5d} ({percentage:5.1f}%)")

    def save_consolidated_dataset(self, output_file="crowelogic_pharma_expanded_training.jsonl"):
        """Save consolidated and expanded training dataset"""
        print(f"\n=== Saving Consolidated Dataset ===\n")

        output_path = Path("training_data") / output_file
        output_path.parent.mkdir(exist_ok=True)

        # Save main JSONL format
        print(f"  Saving to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in self.all_training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        print(f"  ✓ Saved {len(self.all_training_data)} examples")

        # Save Ollama-compatible format
        ollama_path = output_path.parent / output_file.replace('.jsonl', '_ollama.jsonl')
        print(f"\n  Creating Ollama format: {ollama_path}...")
        with open(ollama_path, 'w', encoding='utf-8') as f:
            for example in self.all_training_data:
                ollama_format = {
                    "prompt": example['prompt'],
                    "response": example['response']
                }
                f.write(json.dumps(ollama_format, ensure_ascii=False) + '\n')
        print(f"  ✓ Saved Ollama format")

        # Save statistics
        stats_path = output_path.parent / output_file.replace('.jsonl', '_stats.json')
        print(f"\n  Saving statistics: {stats_path}...")
        stats_data = {
            'total_examples': self.stats['total_examples'],
            'avg_prompt_length': self.stats['avg_prompt_length'],
            'avg_response_length': self.stats['avg_response_length'],
            'by_source': dict(self.stats['by_source']),
            'by_category': dict(self.stats['by_category'])
        }
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved statistics")

        return output_path, ollama_path, stats_path

    def create_requirements_file(self):
        """Create requirements.txt for the project"""
        print("\n=== Creating Requirements File ===\n")

        requirements = """# CroweLogic-Pharma Requirements
# Python 3.8+

# Core dependencies
datasets>=2.14.0
transformers>=4.30.0
huggingface_hub>=0.16.0

# Chemistry and molecular analysis
rdkit-pypi>=2022.9.5

# Data processing
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0

# Machine learning
torch>=2.0.0
tensorflow>=2.13.0  # Optional

# API and web services
requests>=2.31.0
aiohttp>=3.8.5

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
pillow>=10.0.0

# Azure deployment
azure-ai-ml>=1.11.0
azure-identity>=1.14.0
azureml-core>=1.52.0

# Development tools
pytest>=7.4.0
black>=23.7.0
flake8>=6.1.0
"""

        req_path = Path("requirements.txt")
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write(requirements)

        print(f"  ✓ Created {req_path}")
        return req_path

    def run_pipeline(self):
        """Run complete consolidation pipeline"""
        print("=" * 70)
        print("CroweLogic-Pharma Training Data Consolidation Pipeline")
        print("=" * 70)

        # Load all data
        self.load_existing_training_data()
        self.load_new_datasets()

        # Process data
        self.deduplicate()
        self.validate_quality()

        # Generate statistics
        self.calculate_statistics()

        # Save consolidated dataset
        main_file, ollama_file, stats_file = self.save_consolidated_dataset()

        # Create requirements
        req_file = self.create_requirements_file()

        print("\n" + "=" * 70)
        print("Pipeline Complete!")
        print("=" * 70)
        print("\nOutput Files:")
        print(f"  - Main dataset: {main_file}")
        print(f"  - Ollama format: {ollama_file}")
        print(f"  - Statistics: {stats_file}")
        print(f"  - Requirements: {req_file}")

        print("\nNext Steps:")
        print("  1. Review statistics and quality")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Generate expanded dataset: python scripts/generate_dataset.py")
        print("  4. Rebuild model: ollama create CroweLogic-Pharma:latest")
        print("  5. Deploy to Azure: python scripts/deploy_azure.py")

        return {
            'total_examples': self.stats['total_examples'],
            'main_file': main_file,
            'ollama_file': ollama_file,
            'stats_file': stats_file
        }

def main():
    consolidator = TrainingDataConsolidator()
    result = consolidator.run_pipeline()
    return result

if __name__ == "__main__":
    main()
