#!/usr/bin/env python3
"""
Parallel Batch Data Generation
Run this on multiple PCs simultaneously to speed up data collection

Usage Examples:
    # PC 1 - Batch 0 (compounds 0-999)
    python generate_batch.py --batch 0 --batch-size 1000

    # PC 2 - Batch 1 (compounds 1000-1999)
    python generate_batch.py --batch 1 --batch-size 1000

    # PC 3 - Batch 2 (compounds 2000-2999)
    python generate_batch.py --batch 2 --batch-size 1000

    # Resume mode (skip already cached compounds)
    python generate_batch.py --batch 0 --resume

    # Quick test run
    python generate_batch.py --batch 0 --batch-size 100 --test
"""

import sys
import json
import socket
import logging
import argparse
import time
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from data_acquisition.pubchem_fetcher import PubChemFetcher
from data_acquisition.chembl_fetcher import ChEMBLFetcher
from example_generation.mass_scale_generator import MassScaleGenerator, GenerationConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/batch_{time.strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_network_health() -> bool:
    """Check if we can reach external APIs"""
    test_hosts = [
        ('pubchem.ncbi.nlm.nih.gov', 443),
        ('www.ebi.ac.uk', 443),  # ChEMBL
    ]

    logger.info("Checking network connectivity...")
    for host, port in test_hosts:
        try:
            socket.create_connection((host, port), timeout=5)
            logger.info(f"  ✓ {host} - reachable")
        except (socket.gaierror, socket.timeout, OSError) as e:
            logger.error(f"  ✗ {host} - UNREACHABLE: {e}")
            return False

    logger.info("✓ Network health check passed")
    return True


class BatchGenerator:
    """Generate data for a specific batch (for parallel execution)"""

    def __init__(self, batch_id: int, batch_size: int, resume: bool = False, test_mode: bool = False):
        self.batch_id = batch_id
        self.batch_size = batch_size
        self.resume = resume
        self.test_mode = test_mode

        # Calculate offset
        self.offset = batch_id * batch_size

        # Setup output
        self.output_dir = Path("./generated_data/batches")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize fetchers
        self.pubchem = PubChemFetcher()
        self.chembl = ChEMBLFetcher()

        # Stats
        self.stats = {
            'batch_id': batch_id,
            'offset': self.offset,
            'batch_size': batch_size,
            'compounds_fetched': 0,
            'compounds_cached': 0,
            'examples_generated': 0,
            'errors': 0,
            'start_time': time.time(),
        }

    def get_cached_compound_ids(self) -> set:
        """Get IDs of already-cached compounds"""
        cached = set()

        # Check PubChem cache
        pubchem_cache = Path("./cache/pubchem")
        if pubchem_cache.exists():
            cached_files = list(pubchem_cache.glob("*.json"))
            logger.info(f"Found {len(cached_files)} cached PubChem compounds")

        # Check ChEMBL cache
        chembl_cache = Path("./cache/chembl")
        if chembl_cache.exists():
            cached_files = list(chembl_cache.glob("*.json"))
            logger.info(f"Found {len(cached_files)} cached ChEMBL compounds")

        return cached

    def fetch_compounds(self) -> List[Dict]:
        """Fetch compounds for this batch"""
        logger.info(f"\n{'='*70}")
        logger.info(f"BATCH {self.batch_id}: Fetching {self.batch_size} compounds")
        logger.info(f"Offset: {self.offset}")
        logger.info(f"Resume mode: {self.resume}")
        logger.info(f"{'='*70}\n")

        compounds = []

        # Strategy: Mix of ChEMBL and PubChem
        chembl_target = self.batch_size // 2
        pubchem_target = self.batch_size - chembl_target

        # 1. Fetch ChEMBL compounds
        logger.info(f"1. Fetching {chembl_target} ChEMBL compounds...")
        try:
            # Fetch approved drugs
            chembl_ids = self.chembl.fetch_approved_drugs(
                limit=chembl_target,
                offset=self.offset
            )
            logger.info(f"   Found {len(chembl_ids)} ChEMBL IDs")

            for chembl_id in tqdm(chembl_ids, desc="ChEMBL"):
                try:
                    compound = self.chembl.fetch_compound(chembl_id)
                    if compound and self._is_valid_compound(compound):
                        normalized = self._normalize_chembl_compound(compound)
                        compounds.append(normalized)
                        self.stats['compounds_fetched'] += 1
                except Exception as e:
                    logger.debug(f"Failed to fetch {chembl_id}: {e}")
                    self.stats['errors'] += 1
                    continue

        except Exception as e:
            logger.error(f"ChEMBL batch fetch failed: {e}")

        # 2. Fetch PubChem compounds
        logger.info(f"\n2. Fetching {pubchem_target} PubChem compounds...")
        try:
            pubchem_cids = self.pubchem.fetch_common_drugs(limit=pubchem_target)
            logger.info(f"   Found {len(pubchem_cids)} PubChem CIDs")

            # Apply offset to PubChem list
            start_idx = self.offset % len(pubchem_cids) if pubchem_cids else 0
            pubchem_cids = pubchem_cids[start_idx:start_idx + pubchem_target]

            for cid in tqdm(pubchem_cids, desc="PubChem"):
                try:
                    compound = self.pubchem.fetch_compound(cid)
                    if compound and self._is_valid_compound(compound):
                        normalized = self._normalize_pubchem_compound(compound)
                        compounds.append(normalized)
                        self.stats['compounds_fetched'] += 1
                except Exception as e:
                    logger.debug(f"Failed to fetch CID {cid}: {e}")
                    self.stats['errors'] += 1
                    continue

        except Exception as e:
            logger.error(f"PubChem batch fetch failed: {e}")

        logger.info(f"\n✓ Fetched {len(compounds)} valid compounds for batch {self.batch_id}")
        return compounds

    def _is_valid_compound(self, compound: Dict) -> bool:
        """Validate compound has required data"""
        if 'molecule' in compound:  # ChEMBL
            mol = compound['molecule']
            return (mol.get('molecular_formula') and mol.get('molecular_weight'))
        elif 'properties' in compound:  # PubChem
            props = compound['properties']
            return (props.get('molecular_formula') and props.get('molecular_weight'))
        return False

    def _normalize_chembl_compound(self, compound: Dict) -> Dict:
        """Normalize ChEMBL data"""
        mol = compound['molecule']
        max_phase = mol.get('max_phase', 0)
        try:
            max_phase = int(max_phase) if max_phase is not None else 0
        except (ValueError, TypeError):
            max_phase = 0

        return {
            'id': mol['chembl_id'],
            'source': 'chembl',
            'name': mol.get('pref_name', f"Compound {mol['chembl_id']}"),
            'properties': {
                'molecular_formula': mol.get('molecular_formula'),
                'molecular_weight': float(mol.get('molecular_weight', 0)) if mol.get('molecular_weight') else None,
                'canonical_smiles': mol.get('smiles'),
                'logp': float(mol.get('alogp', 0)) if mol.get('alogp') else None,
                'tpsa': float(mol.get('psa', 0)) if mol.get('psa') else None,
                'h_bond_donors': int(mol.get('hbd', 0)) if mol.get('hbd') is not None else None,
                'h_bond_acceptors': int(mol.get('hba', 0)) if mol.get('hba') is not None else None,
                'rotatable_bonds': int(mol.get('rtb', 0)) if mol.get('rtb') is not None else None,
            },
            'metadata': {
                'is_drug': max_phase >= 4,
                'clinical_phase': max_phase,
                'is_natural_product': mol.get('natural_product', False),
                'activity_count': compound.get('activity_count', 0),
            }
        }

    def _normalize_pubchem_compound(self, compound: Dict) -> Dict:
        """Normalize PubChem data"""
        props = compound['properties']
        synonyms = compound.get('synonyms', [])

        return {
            'id': f"CID{compound['cid']}",
            'source': 'pubchem',
            'name': synonyms[0] if synonyms else f"Compound CID{compound['cid']}",
            'properties': {
                'molecular_formula': props.get('molecular_formula'),
                'molecular_weight': float(props.get('molecular_weight', 0)),
                'canonical_smiles': props.get('canonical_smiles'),
                'logp': float(props.get('logp', 0)) if props.get('logp') else None,
                'tpsa': float(props.get('tpsa', 0)) if props.get('tpsa') else None,
                'h_bond_donors': int(props.get('h_bond_donors', 0)) if props.get('h_bond_donors') is not None else None,
                'h_bond_acceptors': int(props.get('h_bond_acceptors', 0)) if props.get('h_bond_acceptors') is not None else None,
                'rotatable_bonds': int(props.get('rotatable_bonds', 0)) if props.get('rotatable_bonds') is not None else None,
            },
            'metadata': {
                'bioactivity_count': compound.get('bioactivity_count', 0),
            }
        }

    def generate_examples(self, compounds: List[Dict]) -> int:
        """Generate training examples from compounds"""
        logger.info(f"\n{'='*70}")
        logger.info(f"Generating examples for batch {self.batch_id}")
        logger.info(f"{'='*70}\n")

        # Configure generator
        examples_per_compound = 10 if not self.test_mode else 5
        config = GenerationConfig(
            target_examples=len(compounds) * examples_per_compound,
            examples_per_compound_min=5,
            examples_per_compound_max=15,
            batch_size=100,
        )

        generator = MassScaleGenerator(config)

        # Generate to file
        output_file = self.output_dir / f"batch_{self.batch_id}.jsonl"
        num_examples = generator.generate_from_compounds(compounds, output_file)

        self.stats['examples_generated'] = num_examples

        logger.info(f"\n✓ Generated {num_examples:,} examples → {output_file}")
        return num_examples

    def save_stats(self):
        """Save batch statistics"""
        self.stats['end_time'] = time.time()
        self.stats['duration_seconds'] = self.stats['end_time'] - self.stats['start_time']

        stats_file = self.output_dir / f"batch_{self.batch_id}_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)

        logger.info(f"\n✓ Stats saved → {stats_file}")

    def run(self):
        """Run the batch generation pipeline"""
        logger.info(f"\n{'='*70}")
        logger.info(f"BATCH GENERATOR - Batch {self.batch_id}")
        logger.info(f"{'='*70}")
        logger.info(f"Machine: {socket.gethostname()}")
        logger.info(f"Batch size: {self.batch_size}")
        logger.info(f"Offset: {self.offset}")
        logger.info(f"Output: {self.output_dir}")
        logger.info(f"{'='*70}\n")

        # Health check
        if not check_network_health():
            logger.error("Network health check failed. Aborting.")
            return

        # Fetch compounds
        compounds = self.fetch_compounds()

        if not compounds:
            logger.error("No compounds fetched. Aborting.")
            return

        # Generate examples
        self.generate_examples(compounds)

        # Save stats
        self.save_stats()

        # Summary
        elapsed = self.stats['duration_seconds']
        logger.info(f"\n{'='*70}")
        logger.info(f"BATCH {self.batch_id} COMPLETE")
        logger.info(f"{'='*70}")
        logger.info(f"✓ Time: {elapsed/60:.1f} minutes")
        logger.info(f"✓ Compounds: {self.stats['compounds_fetched']}")
        logger.info(f"✓ Examples: {self.stats['examples_generated']}")
        logger.info(f"✓ Errors: {self.stats['errors']}")
        logger.info(f"✓ Rate: {self.stats['examples_generated']/elapsed:.1f} examples/sec")
        logger.info(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description='Parallel batch data generation')
    parser.add_argument('--batch', type=int, required=True,
                       help='Batch ID (0, 1, 2, ...) - determines offset')
    parser.add_argument('--batch-size', type=int, default=1000,
                       help='Number of compounds per batch (default: 1000)')
    parser.add_argument('--resume', action='store_true',
                       help='Resume mode: skip already cached compounds')
    parser.add_argument('--test', action='store_true',
                       help='Test mode: smaller batch, fewer examples')

    args = parser.parse_args()

    # Adjust for test mode
    if args.test:
        args.batch_size = min(args.batch_size, 50)
        logger.info("TEST MODE: Running with reduced batch size")

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # Run batch generator
    generator = BatchGenerator(
        batch_id=args.batch,
        batch_size=args.batch_size,
        resume=args.resume,
        test_mode=args.test
    )
    generator.run()


if __name__ == "__main__":
    main()
