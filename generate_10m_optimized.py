#!/usr/bin/env python3
"""
Optimized 10M Dataset Generation
Strategy: Offline-first, high examples-per-compound, resumable

Key improvements:
1. Uses cached compounds (no API dependency)
2. Generates 100-200 examples per compound (vs 5 before)
3. Frequent checkpointing every 10K examples
4. Resume from last checkpoint
5. Graceful error handling
6. Progress monitoring

Target: 10,000,000 examples from 50,000-100,000 compounds
"""

import argparse
import json
import logging
import random
import time
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
import sys

# Import from existing modules
from example_generation.mass_scale_generator import MassScaleGenerator, GenerationConfig, Example
from example_generation.template_library import TemplateLibrary

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/generation_10m.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class Optimized10MGenerator:
    """
    Optimized generator for 10M examples

    Features:
    - Offline compound library (cached data)
    - High-volume template-based generation
    - Frequent checkpointing
    - Resume capability
    - Progress tracking
    """

    def __init__(self, output_dir: str = "./generated_data/massive_10m"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.batches_dir = self.output_dir / "batches"
        self.batches_dir.mkdir(exist_ok=True)

        # State tracking
        self.checkpoint_file = self.output_dir / "checkpoint.json"
        self.state = self.load_checkpoint()

        # Initialize generator with high examples-per-compound
        config = GenerationConfig()
        config.examples_per_compound_min = 100
        config.examples_per_compound_max = 200
        self.generator = MassScaleGenerator(config)

        # Template library
        self.template_lib = TemplateLibrary()

        logger.info("✓ Initialized Optimized 10M Generator")
        logger.info(f"✓ Output directory: {self.output_dir}")
        logger.info(f"✓ Examples per compound: 100-200")

    def load_checkpoint(self) -> Dict:
        """Load generation state from checkpoint"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r') as f:
                state = json.load(f)
                logger.info(f"✓ Loaded checkpoint: {state['examples_generated']:,} examples")
                return state

        # Default state
        return {
            'examples_generated': 0,
            'compounds_processed': 0,
            'current_batch': 1,
            'last_compound_id': None,
            'start_time': time.time(),
        }

    def save_checkpoint(self):
        """Save current generation state"""
        self.state['last_updated'] = time.time()
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def load_cached_compounds(self) -> List[Dict]:
        """
        Load compounds from cache directory

        Looks for:
        - cache/chembl_*.json
        - cache/pubchem_*.json
        - Any existing batch data
        """
        compounds = []
        cache_dir = Path("./cache")

        if not cache_dir.exists():
            logger.warning("No cache directory found. Will use synthetic compounds.")
            return self.generate_synthetic_compounds(50000)

        # Load from cache files
        for cache_file in cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        compounds.append(data)
                    elif isinstance(data, list):
                        compounds.extend(data)
            except Exception as e:
                logger.debug(f"Skipping {cache_file}: {e}")

        logger.info(f"✓ Loaded {len(compounds)} compounds from cache")

        # If not enough, supplement with synthetic
        if len(compounds) < 10000:
            needed = 50000 - len(compounds)
            logger.info(f"Supplementing with {needed:,} synthetic compounds...")
            compounds.extend(self.generate_synthetic_compounds(needed))

        return compounds

    def generate_synthetic_compounds(self, count: int) -> List[Dict]:
        """
        Generate synthetic pharmaceutical compounds for training

        Uses realistic pharmaceutical properties without real compound data
        """
        logger.info(f"Generating {count:,} synthetic compounds...")
        compounds = []

        # Common drug name patterns and components
        prefixes = ["Meta", "Para", "Hyper", "Hypo", "Iso", "Neo", "Pro", "Syn", "Anti"]
        stems = ["ceph", "cycl", "phen", "morph", "sulf", "barb", "benz", "chlor", "fluor"]
        suffixes = ["azole", "olol", "pril", "statin", "cillin", "mycin", "done", "pine"]

        for i in tqdm(range(count), desc="Generating synthetic compounds"):
            # Generate synthetic compound
            name = f"{random.choice(prefixes)}{random.choice(stems)}{random.choice(suffixes)}-{i}"

            compound = {
                'id': f'SYNTH{i:07d}',
                'source': 'synthetic',
                'name': name,
                'properties': {
                    'molecular_formula': self._generate_formula(),
                    'molecular_weight': round(random.uniform(150, 600), 2),
                    'logp': round(random.uniform(-2, 5), 2),
                    'tpsa': round(random.uniform(20, 140), 2),
                    'h_donors': random.randint(0, 5),
                    'h_acceptors': random.randint(1, 10),
                    'rotatable_bonds': random.randint(0, 15),
                    'aromatic_rings': random.randint(0, 4),
                },
                'metadata': {
                    'is_drug': random.random() > 0.3,
                    'clinical_phase': random.randint(0, 4),
                }
            }
            compounds.append(compound)

        logger.info(f"✓ Generated {len(compounds):,} synthetic compounds")
        return compounds

    def _generate_formula(self) -> str:
        """Generate realistic molecular formula"""
        c = random.randint(10, 30)
        h = random.randint(10, 50)
        o = random.randint(1, 10)
        n = random.randint(0, 5)

        formula = f"C{c}H{h}"
        if n > 0:
            formula += f"N{n}"
        if o > 0:
            formula += f"O{o}"

        # Optional elements
        if random.random() > 0.7:
            s = random.randint(1, 2)
            formula += f"S{s}"
        if random.random() > 0.8:
            cl = random.randint(1, 3)
            formula += f"Cl{cl}"

        return formula

    def generate_examples_from_compounds(
        self,
        compounds: List[Dict],
        target_examples: int = 10000000,
        checkpoint_interval: int = 10000
    ):
        """
        Generate training examples from compounds

        Args:
            compounds: List of compound dictionaries
            target_examples: Total examples to generate
            checkpoint_interval: Save checkpoint every N examples
        """
        logger.info("\n" + "=" * 70)
        logger.info("STARTING 10M EXAMPLE GENERATION")
        logger.info("=" * 70)
        logger.info(f"Target: {target_examples:,} examples")
        logger.info(f"Compounds: {len(compounds):,}")
        logger.info(f"Starting from: {self.state['examples_generated']:,} examples")
        logger.info("=" * 70)

        examples_generated = self.state['examples_generated']
        batch_examples = []
        batch_num = self.state['current_batch']

        # Resume from last compound if checkpoint exists
        start_idx = self.state['compounds_processed']

        for idx in tqdm(range(start_idx, len(compounds)), desc="Processing compounds"):
            compound = compounds[idx]

            # Generate 100-200 examples for this compound
            try:
                compound_examples = self.generator._generate_for_compound(compound)

                # Convert Example objects to dicts
                for example_obj in compound_examples:
                    example_dict = {
                        'instruction': example_obj.instruction,
                        'response': example_obj.response,
                        'metadata': {
                            'category': example_obj.category,
                            'source_compound': example_obj.source_compound,
                            'difficulty': example_obj.difficulty,
                            'tags': example_obj.tags,
                        }
                    }
                    batch_examples.append(example_dict)
                    examples_generated += 1

                # Update state
                self.state['examples_generated'] = examples_generated
                self.state['compounds_processed'] = idx + 1

                # Save checkpoint and batch periodically
                if examples_generated % checkpoint_interval == 0:
                    self._save_batch(batch_examples, batch_num)
                    batch_examples = []
                    batch_num += 1
                    self.state['current_batch'] = batch_num
                    self.save_checkpoint()

                    logger.info(f"\n✓ Checkpoint: {examples_generated:,} examples generated")
                    logger.info(f"  Progress: {examples_generated/target_examples*100:.1f}%")
                    logger.info(f"  Compounds processed: {idx+1:,}/{len(compounds):,}")

                # Check if we've reached target
                if examples_generated >= target_examples:
                    logger.info(f"\n✓ Reached target of {target_examples:,} examples!")
                    break

            except Exception as e:
                logger.error(f"Error processing compound {compound.get('id', 'unknown')}: {e}")
                continue

        # Save final batch
        if batch_examples:
            self._save_batch(batch_examples, batch_num)

        # Final stats
        elapsed = time.time() - self.state['start_time']
        logger.info("\n" + "=" * 70)
        logger.info("GENERATION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"✓ Total examples: {examples_generated:,}")
        logger.info(f"✓ Compounds processed: {self.state['compounds_processed']:,}")
        logger.info(f"✓ Batches created: {batch_num}")
        logger.info(f"✓ Total time: {elapsed/3600:.1f} hours")
        logger.info(f"✓ Rate: {examples_generated/(elapsed/3600):.0f} examples/hour")
        logger.info("=" * 70)

    def _save_batch(self, examples: List[Dict], batch_num: int):
        """Save a batch of examples"""
        if not examples:
            return

        batch_file = self.batches_dir / f"batch_{batch_num}.jsonl"
        with open(batch_file, 'w') as f:
            for example in examples:
                f.write(json.dumps(example) + '\n')

        size_mb = batch_file.stat().st_size / 1024 / 1024
        logger.info(f"  Saved batch_{batch_num}: {len(examples):,} examples ({size_mb:.1f} MB)")

    def combine_batches(self, output_file: str = "massive_10m.jsonl"):
        """Combine all batches into final dataset"""
        logger.info("\n" + "=" * 70)
        logger.info("COMBINING BATCHES")
        logger.info("=" * 70)

        output_path = self.output_dir / output_file
        total_examples = 0

        batch_files = sorted(self.batches_dir.glob("batch_*.jsonl"))

        with open(output_path, 'w') as outfile:
            for batch_file in tqdm(batch_files, desc="Combining batches"):
                with open(batch_file, 'r') as infile:
                    for line in infile:
                        outfile.write(line)
                        total_examples += 1

        size_gb = output_path.stat().st_size / 1024 / 1024 / 1024
        logger.info(f"\n✓ Combined dataset created")
        logger.info(f"  File: {output_path}")
        logger.info(f"  Examples: {total_examples:,}")
        logger.info(f"  Size: {size_gb:.2f} GB")

        # Create train/val/test splits
        self._create_splits(output_path, total_examples)

    def _create_splits(self, dataset_file: Path, total_examples: int):
        """Create train/val/test splits"""
        logger.info("\nCreating train/val/test splits...")

        # Read all examples
        examples = []
        with open(dataset_file, 'r') as f:
            for line in f:
                examples.append(json.loads(line))

        # Shuffle
        random.seed(42)
        random.shuffle(examples)

        # Split: 90% train, 5% val, 5% test
        train_size = int(len(examples) * 0.9)
        val_size = int(len(examples) * 0.05)

        splits = {
            'train': examples[:train_size],
            'val': examples[train_size:train_size + val_size],
            'test': examples[train_size + val_size:]
        }

        # Save splits
        for split_name, split_data in splits.items():
            split_file = self.output_dir / f"massive_10m_{split_name}.jsonl"
            with open(split_file, 'w') as f:
                for example in split_data:
                    f.write(json.dumps(example) + '\n')

            size_mb = split_file.stat().st_size / 1024 / 1024
            logger.info(f"  {split_name}: {len(split_data):,} examples ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Optimized 10M dataset generation")
    parser.add_argument('--target', type=int, default=10000000,
                       help='Target number of examples (default: 10,000,000)')
    parser.add_argument('--checkpoint-interval', type=int, default=10000,
                       help='Save checkpoint every N examples (default: 10,000)')
    parser.add_argument('--output-dir', type=str, default='./generated_data/massive_10m',
                       help='Output directory')
    parser.add_argument('--combine-only', action='store_true',
                       help='Only combine existing batches (no generation)')

    args = parser.parse_args()

    # Initialize generator
    generator = Optimized10MGenerator(output_dir=args.output_dir)

    if args.combine_only:
        # Just combine existing batches
        generator.combine_batches()
    else:
        # Load compounds and generate
        compounds = generator.load_cached_compounds()

        if not compounds:
            logger.error("No compounds available. Cannot generate dataset.")
            return

        # Generate examples
        generator.generate_examples_from_compounds(
            compounds=compounds,
            target_examples=args.target,
            checkpoint_interval=args.checkpoint_interval
        )

        # Combine batches
        generator.combine_batches()

    logger.info("\n✓ Generation complete!")


if __name__ == "__main__":
    main()
