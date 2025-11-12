#!/usr/bin/env python3
"""
CroweLogic Dataset Curator
Implements quality scoring, watermarking, and tier assignment

Usage:
    python3 crowelogic_curator.py --input generated_data/fast_10m/fast_10m.jsonl \
                                   --output crowelogic_curated/ \
                                   --sample 10000
"""

import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import re


class CroweLogicCurator:
    """
    Curates pharmaceutical training datasets with:
    - Quality scoring
    - IP watermarking
    - Tier assignment
    - Metadata enrichment
    """

    VERSION = "1.0-crowelogic"
    GENESIS_DATE = "2025-11-12"
    SECRET_KEY = "crowelogic-pharma-2025"  # In production, use env variable

    def __init__(self):
        self.compound_registry = set()
        self.template_registry = set()
        self.statistics = defaultdict(int)

    def score_scientific_accuracy(self, example: Dict) -> float:
        """
        Score scientific accuracy (0-100)
        - Valid chemical properties
        - Consistent units
        - Realistic values
        """
        score = 100.0
        response = example.get('response', '')

        # Check for proper units
        if 'g/mol' in response or 'Da' in response:
            score += 5
        if 'logP' in response and re.search(r'logP.*?[-\d.]+', response):
            score += 5
        if 'TPSA' in response and re.search(r'TPSA.*?[\d.]+', response):
            score += 5

        # Check for chemical formula format
        if re.search(r'C\d+H\d+[NOSPFClBrI\d]*', response):
            score += 10

        # Penalize for missing critical information
        if len(response) < 50:
            score -= 20
        if 'unknown' in response.lower() or 'n/a' in response.lower():
            score -= 15

        # Check metadata completeness
        metadata = example.get('metadata', {})
        if 'compound' in metadata:
            score += 5
        if 'template' in metadata:
            score += 5
        if 'batch' in metadata:
            score += 5

        return max(0, min(100, score))

    def score_linguistic_quality(self, example: Dict) -> float:
        """
        Score linguistic quality (0-100)
        - Grammar
        - Clarity
        - Professional language
        """
        score = 80.0  # Base score

        instruction = example.get('instruction', '')
        response = example.get('response', '')

        # Length checks (not too short, not too long)
        if 30 < len(response) < 500:
            score += 10
        elif len(response) < 30:
            score -= 20

        # Proper capitalization
        if response and response[0].isupper():
            score += 5

        # Ends with period
        if response and response.rstrip()[-1] in '.!?':
            score += 5

        # Contains pharmaceutical terminology
        pharma_terms = ['molecular', 'compound', 'bioavailability', 'logP',
                       'TPSA', 'pharmacokinetic', 'therapeutic', 'drug']
        if any(term in response.lower() for term in pharma_terms):
            score += 10

        # Avoid repetition
        words = response.lower().split()
        if len(words) > 0 and len(set(words)) / len(words) > 0.7:
            score += 5

        return max(0, min(100, score))

    def score_training_value(self, example: Dict) -> float:
        """
        Score training value (0-100)
        - Information density
        - Reasoning complexity
        - Educational value
        """
        score = 70.0  # Base score

        response = example.get('response', '')
        instruction = example.get('instruction', '')

        # Information density
        if len(response.split()) > 20:
            score += 10
        if len(response.split()) > 40:
            score += 10

        # Numerical data present
        numbers = re.findall(r'[\d.]+', response)
        if len(numbers) >= 3:
            score += 10
        if len(numbers) >= 5:
            score += 5

        # Explanatory language (shows reasoning)
        reasoning_words = ['because', 'therefore', 'indicates', 'suggests',
                          'demonstrates', 'shows', 'compared to', 'due to']
        if any(word in response.lower() for word in reasoning_words):
            score += 15

        # Complex questions (require deeper knowledge)
        complex_words = ['analyze', 'compare', 'evaluate', 'assess', 'how']
        if any(word in instruction.lower() for word in complex_words):
            score += 10

        return max(0, min(100, score))

    def score_uniqueness(self, example: Dict) -> float:
        """
        Score uniqueness (0-100)
        - Novel compound names
        - Template diversity
        - Non-redundant information
        """
        score = 75.0  # Base score

        metadata = example.get('metadata', {})
        compound = metadata.get('compound', '')
        template = metadata.get('template', '')

        # Track compound frequency
        if compound:
            if compound not in self.compound_registry:
                score += 15
                self.compound_registry.add(compound)
            else:
                score -= 10  # Penalize duplicates

        # Track template diversity
        if template:
            if template not in self.template_registry:
                score += 10
                self.template_registry.add(template)

        return max(0, min(100, score))

    def calculate_composite_score(self, example: Dict) -> Tuple[float, Dict]:
        """
        Calculate weighted composite quality score
        Returns: (total_score, component_scores)
        """
        scientific = self.score_scientific_accuracy(example)
        linguistic = self.score_linguistic_quality(example)
        training = self.score_training_value(example)
        uniqueness = self.score_uniqueness(example)

        # Weighted average
        total_score = (
            scientific * 0.35 +
            linguistic * 0.20 +
            training * 0.25 +
            uniqueness * 0.20
        )

        components = {
            'scientific_accuracy': scientific,
            'linguistic_quality': linguistic,
            'training_value': training,
            'uniqueness_score': uniqueness,
            'total_score': total_score
        }

        return total_score, components

    def assign_quality_tier(self, total_score: float) -> str:
        """Assign quality tier based on total score"""
        if total_score >= 90:
            return "GOLD"
        elif total_score >= 75:
            return "SILVER"
        elif total_score >= 60:
            return "BRONZE"
        else:
            return "TRAINING"

    def generate_signature(self, example: Dict, index: int) -> Dict:
        """
        Generate cryptographic signature for watermarking
        """
        # Create unique ID
        content_hash = hashlib.sha256(
            json.dumps(example, sort_keys=True).encode()
        ).hexdigest()

        # Batch fingerprint
        batch = example.get('metadata', {}).get('batch', 0)
        batch_hash = hashlib.sha256(
            f"{batch}-{self.SECRET_KEY}".encode()
        ).hexdigest()[:16]

        # Template DNA
        template = example.get('metadata', {}).get('template', '')
        template_hash = hashlib.sha256(
            f"{template}-{self.SECRET_KEY}".encode()
        ).hexdigest()[:16]

        # Temporal marker
        timestamp = datetime.now().isoformat()

        return {
            'cl_id': f"CL-{index:08d}-{content_hash[:16]}",
            'cl_version': self.VERSION,
            'cl_genesis': self.GENESIS_DATE,
            'cl_timestamp': timestamp,
            'cl_batch_hash': batch_hash,
            'cl_template_dna': template_hash,
            'cl_signature': hashlib.sha256(
                f"{content_hash}-{batch_hash}-{template_hash}-{self.SECRET_KEY}".encode()
            ).hexdigest()
        }

    def enrich_metadata(self, example: Dict, index: int, scores: Dict, tier: str) -> Dict:
        """
        Add comprehensive CroweLogic metadata
        """
        # Determine domain from template
        template = example.get('metadata', {}).get('template', '').lower()
        domain = self._classify_domain(template, example.get('instruction', '').lower())

        # Generate watermark
        signature = self.generate_signature(example, index)

        # Add CroweLogic metadata
        crowelogic_meta = {
            'quality_tier': tier,
            **scores,
            'domain': domain,
            'difficulty_level': self._assess_difficulty(scores['training_value']),
            'recommended_use': self._recommend_use(tier),
            'citation': f"CroweLogic Pharmaceutical AI Training Dataset v{self.VERSION}",
            'license': 'CroweLogic-Proprietary-2025',
            '_watermark': signature
        }

        # Merge into existing metadata
        if 'metadata' not in example:
            example['metadata'] = {}

        example['metadata']['crowelogic'] = crowelogic_meta

        return example

    def _classify_domain(self, template: str, instruction: str) -> str:
        """Classify example into pharmaceutical domain"""
        text = template + " " + instruction

        if any(word in text for word in ['molecular', 'formula', 'weight', 'logp', 'tpsa']):
            return 'molecular_properties'
        elif any(word in text for word in ['pharmacokinetic', 'adme', 'bioavailability']):
            return 'pharmacokinetics'
        elif any(word in text for word in ['lipinski', 'rule of five', 'drug-like']):
            return 'drug_likeness'
        elif any(word in text for word in ['indication', 'treatment', 'dose', 'clinical']):
            return 'clinical_applications'
        elif any(word in text for word in ['target', 'binding', 'inhibit', 'activity']):
            return 'drug_discovery'
        else:
            return 'general_pharmaceutical'

    def _assess_difficulty(self, training_value: float) -> str:
        """Assess difficulty level"""
        if training_value >= 90:
            return 'advanced'
        elif training_value >= 75:
            return 'intermediate'
        else:
            return 'basic'

    def _recommend_use(self, tier: str) -> List[str]:
        """Recommend use cases based on tier"""
        if tier == "GOLD":
            return ['fine-tuning', 'evaluation', 'benchmarking', 'commercial']
        elif tier == "SILVER":
            return ['fine-tuning', 'evaluation', 'research']
        elif tier == "BRONZE":
            return ['training', 'augmentation', 'research']
        else:
            return ['pre-training', 'internal_testing']

    def curate_dataset(self, input_file: Path, output_dir: Path, sample_size: int = None):
        """
        Main curation pipeline
        """
        print(f"🔬 CroweLogic Dataset Curator v{self.VERSION}")
        print(f"=" * 70)
        print(f"Input: {input_file}")
        print(f"Output: {output_dir}")
        print(f"Sample: {sample_size if sample_size else 'ALL'}")
        print()

        output_dir.mkdir(parents=True, exist_ok=True)

        # Output files for each tier
        tier_files = {
            'GOLD': output_dir / 'crowelogic_gold.jsonl',
            'SILVER': output_dir / 'crowelogic_silver.jsonl',
            'BRONZE': output_dir / 'crowelogic_bronze.jsonl',
            'TRAINING': output_dir / 'crowelogic_training.jsonl'
        }

        tier_handles = {
            tier: open(file, 'w') for tier, file in tier_files.items()
        }

        # Process dataset
        processed = 0
        tier_counts = defaultdict(int)
        score_distribution = []

        try:
            with open(input_file, 'r') as f:
                for i, line in enumerate(f):
                    if sample_size and i >= sample_size:
                        break

                    example = json.loads(line)

                    # Calculate scores
                    total_score, component_scores = self.calculate_composite_score(example)
                    tier = self.assign_quality_tier(total_score)

                    # Enrich metadata
                    enriched = self.enrich_metadata(example, i, component_scores, tier)

                    # Write to appropriate tier file
                    tier_handles[tier].write(json.dumps(enriched) + '\n')

                    # Statistics
                    tier_counts[tier] += 1
                    score_distribution.append(total_score)
                    processed += 1

                    if processed % 10000 == 0:
                        print(f"Processed {processed:,} examples...")

        finally:
            for handle in tier_handles.values():
                handle.close()

        # Print summary
        print()
        print(f"✅ Curation Complete!")
        print(f"=" * 70)
        print(f"Total Processed: {processed:,}")
        print()
        print(f"Quality Tier Distribution:")
        for tier in ['GOLD', 'SILVER', 'BRONZE', 'TRAINING']:
            count = tier_counts[tier]
            pct = (count / processed * 100) if processed > 0 else 0
            print(f"  {tier:10s}: {count:8,} ({pct:5.1f}%) → {tier_files[tier]}")

        print()
        print(f"Score Statistics:")
        if score_distribution:
            print(f"  Mean:   {sum(score_distribution) / len(score_distribution):.1f}")
            print(f"  Median: {sorted(score_distribution)[len(score_distribution)//2]:.1f}")
            print(f"  Min:    {min(score_distribution):.1f}")
            print(f"  Max:    {max(score_distribution):.1f}")

        print()
        print(f"Unique Compounds: {len(self.compound_registry):,}")
        print(f"Unique Templates: {len(self.template_registry):,}")

        # Generate manifest
        manifest = {
            'version': self.VERSION,
            'genesis_date': self.GENESIS_DATE,
            'curation_date': datetime.now().isoformat(),
            'total_examples': processed,
            'tier_distribution': dict(tier_counts),
            'unique_compounds': len(self.compound_registry),
            'unique_templates': len(self.template_registry),
            'tier_files': {tier: str(file) for tier, file in tier_files.items()},
            'score_statistics': {
                'mean': sum(score_distribution) / len(score_distribution) if score_distribution else 0,
                'median': sorted(score_distribution)[len(score_distribution)//2] if score_distribution else 0,
                'min': min(score_distribution) if score_distribution else 0,
                'max': max(score_distribution) if score_distribution else 0
            }
        }

        manifest_file = output_dir / 'crowelogic_manifest.json'
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        print()
        print(f"📄 Manifest: {manifest_file}")
        print()
        print(f"🎓 CroweLogic Curation Complete!")


def main():
    parser = argparse.ArgumentParser(description='CroweLogic Dataset Curator')
    parser.add_argument('--input', type=str, required=True,
                       help='Input JSONL dataset file')
    parser.add_argument('--output', type=str, required=True,
                       help='Output directory for curated datasets')
    parser.add_argument('--sample', type=int, default=None,
                       help='Sample size (process first N examples, default: all)')

    args = parser.parse_args()

    curator = CroweLogicCurator()
    curator.curate_dataset(
        Path(args.input),
        Path(args.output),
        args.sample
    )


if __name__ == '__main__':
    main()
