#!/usr/bin/env python3
"""
Massive-Scale Training Data Generation
Target: 10,000,000+ examples for 70B model training

This script orchestrates massive-scale data generation from multiple sources:
- ChEMBL: 100,000+ compounds (approved drugs, natural products, bioactive)
- DrugBank: 14,000 approved drugs
- COCONUT: 400,000 natural products
- PubChem: Additional coverage

Generates examples using 200+ templates across 12 pharmaceutical domains.
"""

import argparse
import json
import logging
import random
import time
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

# Import fetchers
from data_acquisition.chembl_fetcher import ChEMBLFetcher
from data_acquisition.drugbank_fetcher import DrugBankFetcher
from data_acquisition.pubchem_fetcher import PubChemFetcher
try:
    from data_acquisition.coconut_fetcher import COCONUTFetcher
    COCONUT_AVAILABLE = True
except ImportError:
    COCONUT_AVAILABLE = False
    logging.warning("COCONUT fetcher not available")

# Import generation
from example_generation.mass_scale_generator import MassScaleGenerator, GenerationConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MassiveDatasetGenerator:
    """
    Orchestrates massive-scale dataset generation

    Target: 10M+ examples from 1M+ compounds
    """

    def __init__(self, output_dir: str = "./generated_data/massive"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize fetchers
        logger.info("Initializing data fetchers...")
        self.chembl = ChEMBLFetcher()
        self.drugbank = DrugBankFetcher()
        self.pubchem = PubChemFetcher()
        if COCONUT_AVAILABLE:
            self.coconut = COCONUTFetcher()

        # Initialize generator
        logger.info("Initializing example generator...")
        config = GenerationConfig()
        config.target_examples = target_examples if 'target_examples' in locals() else 10000000
        self.generator = MassScaleGenerator(config)

        # Statistics
        self.stats = {
            'compounds_fetched': 0,
            'examples_generated': 0,
            'sources': {},
            'categories': {},
        }

    def fetch_compounds_phase_1(self, target: int = 100000) -> List[Dict]:
        """
        Phase 1: Fetch 100K diverse compounds

        Sources:
        - ChEMBL approved drugs: 14,000
        - ChEMBL natural products: 50,000
        - ChEMBL bioactive: 36,000
        - DrugBank: As backup

        Returns:
            List of compound dictionaries
        """
        compounds = []

        logger.info("\n" + "=" * 70)
        logger.info("PHASE 1: Fetching 100,000 Diverse Compounds")
        logger.info("=" * 70)

        # 1. ChEMBL Approved Drugs (14K target)
        logger.info("\n1. Fetching ChEMBL approved drugs...")
        try:
            approved_ids = self.chembl.fetch_approved_drugs_all(max_total=14000)
            logger.info(f"   Found {len(approved_ids)} approved drugs")

            for chembl_id in tqdm(approved_ids, desc="Fetching approved drug details"):
                compound = self.chembl.fetch_compound(chembl_id)
                if compound:
                    normalized = self._normalize_chembl_data(compound)
                    if normalized:
                        compounds.append(normalized)
                        self.stats['sources']['chembl_approved'] = self.stats['sources'].get('chembl_approved', 0) + 1

                if len(compounds) >= target:
                    break

        except Exception as e:
            logger.error(f"Error fetching approved drugs: {e}")

        # 2. ChEMBL Natural Products (if needed - to be implemented)
        if len(compounds) < target:
            logger.info(f"\n2. Natural products: Fetching additional compounds...")
            logger.info(f"   Current total: {len(compounds)}, need {target - len(compounds)} more")

            try:
                # Use existing fetch_natural_products method with pagination
                batch_size = 100
                offset = 0
                remaining = target - len(compounds)

                while len(compounds) < target:
                    natural_ids = self.chembl.fetch_natural_products(limit=batch_size, offset=offset)
                    if not natural_ids:
                        break

                    for chembl_id in tqdm(natural_ids, desc=f"Fetching natural products (offset {offset})"):
                        compound = self.chembl.fetch_compound(chembl_id)
                        if compound:
                            normalized = self._normalize_chembl_data(compound)
                            if normalized:
                                compounds.append(normalized)
                                self.stats['sources']['chembl_natural'] = self.stats['sources'].get('chembl_natural', 0) + 1

                        if len(compounds) >= target:
                            break

                    offset += batch_size

                    if len(compounds) >= target:
                        break

            except Exception as e:
                logger.error(f"Error fetching natural products: {e}")

        logger.info(f"\n✓ Phase 1 Complete: Fetched {len(compounds)} compounds")
        logger.info(f"  Source distribution: {self.stats['sources']}")

        self.stats['compounds_fetched'] = len(compounds)
        return compounds

    def _normalize_chembl_data(self, compound: Dict) -> Dict:
        """Normalize ChEMBL data to standard format"""
        try:
            props = compound.get('properties', {})

            normalized = {
                'id': compound.get('molecule_chembl_id'),
                'source': 'chembl',
                'name': compound.get('pref_name', compound.get('molecule_chembl_id')),
                'properties': {
                    'molecular_formula': props.get('molecular_formula'),
                    'molecular_weight': props.get('molecular_weight'),
                    'canonical_smiles': props.get('canonical_smiles'),
                    'logp': props.get('alogp'),
                    'tpsa': props.get('psa'),
                    'h_donors': props.get('hbd'),
                    'h_acceptors': props.get('hba'),
                    'rotatable_bonds': props.get('rtb'),
                    'aromatic_rings': props.get('aromatic_rings'),
                },
                'metadata': {
                    'is_drug': compound.get('max_phase', 0) >= 4,
                    'clinical_phase': compound.get('max_phase', 0),
                    'is_natural_product': compound.get('natural_product', 0) == 1,
                }
            }

            return normalized
        except Exception as e:
            logger.debug(f"Failed to normalize compound: {e}")
            return None

    def generate_examples_from_compounds(
        self,
        compounds: List[Dict],
        total_target: int = 10000000
    ) -> List[Dict]:
        """
        Generate training examples from compounds

        Args:
            compounds: List of compound dictionaries
            total_target: Total examples target

        Returns:
            List of training examples (as dicts, not Example objects)
        """
        logger.info("\n" + "=" * 70)
        logger.info(f"GENERATING EXAMPLES: Target {total_target:,} examples")
        logger.info("=" * 70)

        all_examples = []

        logger.info(f"Processing {len(compounds)} compounds...")

        # Generate examples using MassScaleGenerator
        for compound in tqdm(compounds, desc="Generating examples"):
            # Use generator's _generate_for_compound method
            example_objects = self.generator._generate_for_compound(compound)

            # Convert Example objects to dicts
            for example_obj in example_objects:
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
                all_examples.append(example_dict)

                # Track categories
                self.stats['categories'][example_obj.category] = self.stats['categories'].get(example_obj.category, 0) + 1

            # Check if we've reached target
            if len(all_examples) >= total_target:
                logger.info(f"\n✓ Reached target of {total_target:,} examples!")
                break

            # Save intermediate results periodically
            if len(all_examples) % 10000 == 0 and len(all_examples) > 0:
                self._save_intermediate(all_examples)

        logger.info(f"\n✓ Generated {len(all_examples):,} total examples")
        logger.info(f"  Category distribution: {self.stats['categories']}")

        self.stats['examples_generated'] = len(all_examples)
        return all_examples[:total_target]

    def _save_intermediate(self, examples: List[Dict]):
        """Save intermediate results to prevent data loss"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        checkpoint_file = self.output_dir / f"checkpoint_{timestamp}.jsonl"

        with open(checkpoint_file, 'w') as f:
            for example in examples:
                f.write(json.dumps(example) + '\n')

        logger.info(f"   Checkpoint saved: {len(examples):,} examples → {checkpoint_file}")

    def save_final_dataset(self, examples: List[Dict], filename: str = "massive_10m.jsonl"):
        """Save final dataset with metadata"""
        output_file = self.output_dir / filename

        logger.info(f"\nSaving final dataset to {output_file}...")

        with open(output_file, 'w') as f:
            for example in tqdm(examples, desc="Writing examples"):
                f.write(json.dumps(example) + '\n')

        # Save metadata
        metadata_file = self.output_dir / f"{filename}.metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

        # Create splits
        self._create_splits(examples, filename)

        logger.info(f"✓ Dataset saved: {len(examples):,} examples")
        logger.info(f"✓ File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
        logger.info(f"✓ Metadata: {metadata_file}")

    def _create_splits(self, examples: List[Dict], base_filename: str):
        """Create train/val/test splits"""
        logger.info("\nCreating train/val/test splits (80/10/10)...")

        random.seed(42)
        random.shuffle(examples)

        train_size = int(len(examples) * 0.8)
        val_size = int(len(examples) * 0.1)

        train_set = examples[:train_size]
        val_set = examples[train_size:train_size + val_size]
        test_set = examples[train_size + val_size:]

        # Save splits
        for split_name, split_data in [
            ('train', train_set),
            ('val', val_set),
            ('test', test_set)
        ]:
            split_file = self.output_dir / f"{base_filename.replace('.jsonl', '')}_{split_name}.jsonl"
            with open(split_file, 'w') as f:
                for example in split_data:
                    f.write(json.dumps(example) + '\n')

            logger.info(f"  {split_name}: {len(split_data):,} examples → {split_file}")

    def run(self, target_examples: int = 10000000, target_compounds: int = 100000):
        """
        Run massive-scale generation pipeline

        Args:
            target_examples: Total examples to generate (default 10M)
            target_compounds: Compounds to fetch (default 100K)
        """
        logger.info("\n" + "=" * 70)
        logger.info("MASSIVE-SCALE DATASET GENERATION")
        logger.info("=" * 70)
        logger.info(f"Target: {target_examples:,} examples from {target_compounds:,} compounds")
        logger.info(f"Output: {self.output_dir}")
        logger.info("=" * 70)

        start_time = time.time()

        # Phase 1: Fetch compounds
        compounds = self.fetch_compounds_phase_1(target=target_compounds)

        # Phase 2: Generate examples
        examples = self.generate_examples_from_compounds(
            compounds=compounds,
            total_target=target_examples
        )

        # Phase 3: Save results
        self.save_final_dataset(examples)

        # Final summary
        elapsed = time.time() - start_time
        logger.info("\n" + "=" * 70)
        logger.info("GENERATION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"✓ Total time: {elapsed / 3600:.1f} hours")
        logger.info(f"✓ Compounds: {self.stats['compounds_fetched']:,}")
        logger.info(f"✓ Examples: {self.stats['examples_generated']:,}")
        logger.info(f"✓ Avg examples/compound: {self.stats['examples_generated'] / max(self.stats['compounds_fetched'], 1):.1f}")
        logger.info(f"✓ Generation rate: {self.stats['examples_generated'] / max(elapsed, 1):.1f} examples/second")
        logger.info("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Massive-scale pharmaceutical dataset generation")
    parser.add_argument('--target-examples', type=int, default=10000000,
                       help='Target number of examples (default: 10,000,000)')
    parser.add_argument('--target-compounds', type=int, default=100000,
                       help='Target number of compounds to fetch (default: 100,000)')
    parser.add_argument('--output-dir', type=str, default='./generated_data/massive',
                       help='Output directory (default: ./generated_data/massive)')

    args = parser.parse_args()

    generator = MassiveDatasetGenerator(output_dir=args.output_dir)
    generator.run(
        target_examples=args.target_examples,
        target_compounds=args.target_compounds
    )


if __name__ == "__main__":
    main()
