#!/usr/bin/env python3
"""
Training Data Generation Orchestrator
Fetches compounds from multiple sources and generates training examples

Usage:
    python generate_training_data.py --target 10000 --output datasets/multi_source_10k.jsonl
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Set
from tqdm import tqdm

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from data_acquisition.pubchem_fetcher import PubChemFetcher
from data_acquisition.chembl_fetcher import ChEMBLFetcher
from example_generation.mass_scale_generator import MassScaleGenerator, GenerationConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataOrchestrator:
    """
    Orchestrate multi-source data fetching and example generation
    """

    def __init__(self, target_compounds: int = 500, offset: int = 0):
        self.target_compounds = target_compounds
        self.offset = offset
        self.pubchem = PubChemFetcher()
        self.chembl = ChEMBLFetcher()
        self.compounds = []

    def fetch_compounds(self):
        """Fetch compounds from multiple sources"""
        logger.info(f"Fetching up to {self.target_compounds} compounds from multiple sources (offset={self.offset})...")

        # Strategy: ULTRA-AGGRESSIVE multi-source fetching for 200K+ dataset
        logger.info("1. Fetching approved drugs from ChEMBL...")
        chembl_drugs = self.chembl.fetch_approved_drugs(
            limit=min(1000, self.target_compounds // 2),
            offset=self.offset
        )
        logger.info(f"   Found {len(chembl_drugs)} ChEMBL drug IDs")

        logger.info("2. Fetching natural products from ChEMBL (MASSIVE SCALE)...")
        chembl_natural = self.chembl.fetch_natural_products(
            limit=min(1000, self.target_compounds // 2),
            offset=self.offset
        )
        logger.info(f"   Found {len(chembl_natural)} ChEMBL natural product IDs")

        logger.info("3. Fetching common drugs from PubChem (200+ drug list)...")
        pubchem_drugs = self.pubchem.fetch_common_drugs(limit=min(200, self.target_compounds // 4))
        logger.info(f"   Found {len(pubchem_drugs)} PubChem drug CIDs")

        # Fetch detailed data for each compound
        all_compound_ids = {
            'chembl': chembl_drugs + chembl_natural,
            'pubchem': pubchem_drugs,
        }

        logger.info(f"\n4. Fetching detailed compound data...")
        for source, ids in all_compound_ids.items():
            logger.info(f"   Processing {len(ids)} {source} compounds...")

            if source == 'chembl':
                for chembl_id in tqdm(ids[:self.target_compounds], desc=f"ChEMBL"):
                    try:
                        compound = self.chembl.fetch_compound(chembl_id)
                        if compound and self._is_valid_compound(compound):
                            normalized = self._normalize_chembl_compound(compound)
                            self.compounds.append(normalized)
                    except Exception as e:
                        logger.debug(f"Failed to fetch {chembl_id}: {e}")
                        continue

            elif source == 'pubchem':
                for cid in tqdm(ids[:self.target_compounds], desc=f"PubChem"):
                    try:
                        compound = self.pubchem.fetch_compound(cid)
                        if compound and self._is_valid_compound(compound):
                            normalized = self._normalize_pubchem_compound(compound)
                            self.compounds.append(normalized)
                    except Exception as e:
                        logger.debug(f"Failed to fetch {cid}: {e}")
                        continue

            if len(self.compounds) >= self.target_compounds:
                break

        logger.info(f"\n✓ Fetched {len(self.compounds)} valid compounds")
        return self.compounds

    def _is_valid_compound(self, compound: Dict) -> bool:
        """Validate compound has required data"""
        # Must have basic molecular data
        if 'molecule' in compound:  # ChEMBL
            mol = compound['molecule']
            return (mol.get('molecular_formula') and
                   mol.get('molecular_weight'))
        elif 'properties' in compound:  # PubChem
            props = compound['properties']
            return (props.get('molecular_formula') and
                   props.get('molecular_weight'))
        return False

    def _normalize_chembl_compound(self, compound: Dict) -> Dict:
        """Normalize ChEMBL data to standard format"""
        mol = compound['molecule']

        # Safely convert max_phase to int
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
                'has_mechanism': len(compound.get('mechanisms', [])) > 0,
            }
        }

    def _normalize_pubchem_compound(self, compound: Dict) -> Dict:
        """Normalize PubChem data to standard format"""
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


def main():
    parser = argparse.ArgumentParser(description='Generate training data from multiple sources')
    parser.add_argument('--compounds', type=int, default=500, help='Number of compounds to fetch')
    parser.add_argument('--examples', type=int, default=5000, help='Target number of examples')
    parser.add_argument('--output', type=str, default='datasets/multi_source_dataset.jsonl', help='Output file')
    args = parser.parse_args()

    print("="*70)
    print("Multi-Source Training Data Generation")
    print("="*70)
    print(f"\nTarget: {args.compounds} compounds → {args.examples} examples")
    print(f"Output: {args.output}\n")

    # 1. Fetch compounds
    orchestrator = DataOrchestrator(target_compounds=args.compounds)
    compounds = orchestrator.fetch_compounds()

    if not compounds:
        logger.error("No compounds fetched. Exiting.")
        return

    # 2. Generate examples
    logger.info(f"\n{'='*70}")
    logger.info("Generating training examples...")
    logger.info(f"{'='*70}\n")

    config = GenerationConfig(
        target_examples=args.examples,
        examples_per_compound_min=5,
        examples_per_compound_max=20,
        batch_size=500,
    )

    generator = MassScaleGenerator(config)
    output_path = Path(args.output)

    num_examples = generator.generate_from_compounds(compounds, output_path)

    # 3. Statistics
    print(f"\n{'='*70}")
    print("Generation Complete!")
    print(f"{'='*70}")
    print(f"\n✓ Fetched: {len(compounds)} compounds")
    print(f"✓ Generated: {num_examples:,} examples")
    print(f"✓ Output: {output_path}")
    print(f"\nFile size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Print sample
    print(f"\n{'='*70}")
    print("Sample Examples:")
    print(f"{'='*70}\n")

    with open(output_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= 3:
                break
            example = json.loads(line)
            print(f"Q: {example['instruction']}")
            print(f"A: {example['response'][:150]}...")
            print("-"*70)

    # Source statistics
    print(f"\nSource Distribution:")
    source_counts = {}
    for compound in compounds:
        source = compound['source']
        source_counts[source] = source_counts.get(source, 0) + 1

    for source, count in source_counts.items():
        print(f"  {source}: {count} compounds ({count/len(compounds)*100:.1f}%)")


if __name__ == "__main__":
    main()
