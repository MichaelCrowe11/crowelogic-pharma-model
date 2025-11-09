#!/usr/bin/env python3
"""
ChEMBL Data Fetcher
Fetch bioactive compound data from ChEMBL database (2.4M+ compounds)
API Docs: https://www.ebi.ac.uk/chembl/api/data/docs
"""

import logging
from typing import Dict, List, Optional
from .base_fetcher import BaseFetcher, FetcherConfig

logger = logging.getLogger(__name__)


class ChEMBLFetcher(BaseFetcher):
    """
    Fetch bioactive compound data from ChEMBL database

    Data Available:
    - Bioactive molecules: 2.4M+
    - Bioassay activities: 20M+
    - Drug targets: 15K+
    - Mechanism of action data
    - ADME properties
    - Clinical trial data
    - Target-based activities (IC50, EC50, Ki, etc.)
    """

    @property
    def source_name(self) -> str:
        return "chembl"

    @property
    def base_url(self) -> str:
        return "https://www.ebi.ac.uk/chembl/api/data"

    @property
    def default_headers(self) -> Dict[str, str]:
        """ChEMBL requires specific headers"""
        return {
            'User-Agent': 'CroweLogic-Pharma/2.0 (Educational Research)',
            'Accept': 'application/json',
        }

    def fetch_compound(self, chembl_id: str) -> Optional[Dict]:
        """
        Fetch compound data by ChEMBL ID

        Args:
            chembl_id: ChEMBL molecule ID (e.g., "CHEMBL25" for aspirin)

        Returns:
            Compound data with properties, activities, and targets
        """
        cache_key = f"molecule_{chembl_id}"
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached

        try:
            # Fetch molecule data
            molecule = self._fetch_molecule(chembl_id)
            if not molecule:
                return None

            # Fetch bioactivities
            activities = self._fetch_activities(chembl_id)

            # Fetch mechanism of action (if drug)
            mechanisms = self._fetch_mechanisms(chembl_id)

            # Compile compound data
            compound_data = {
                'source': 'chembl',
                'chembl_id': chembl_id,
                'molecule': molecule,
                'activities': activities[:20],  # Top 20 activities
                'activity_count': len(activities),
                'mechanisms': mechanisms,
                'drug_data': self._extract_drug_data(molecule),
            }

            self._save_to_cache(cache_key, compound_data)
            return compound_data

        except Exception as e:
            logger.error(f"Failed to fetch ChEMBL ID {chembl_id}: {e}")
            return None

    def _fetch_molecule(self, chembl_id: str) -> Optional[Dict]:
        """Fetch molecule core data"""
        url = f"{self.base_url}/molecule/{chembl_id}.json"

        try:
            data = self._make_request(url)
            if 'molecule_chembl_id' in data:
                return {
                    'chembl_id': data.get('molecule_chembl_id'),
                    'pref_name': data.get('pref_name'),
                    'molecule_type': data.get('molecule_type'),
                    'max_phase': data.get('max_phase'),  # Clinical trial phase (0-4)
                    'therapeutic_flag': data.get('therapeutic_flag'),
                    'natural_product': data.get('natural_product'),
                    'molecular_formula': data.get('molecule_properties', {}).get('full_molformula'),
                    'molecular_weight': data.get('molecule_properties', {}).get('full_mwt'),
                    'smiles': data.get('molecule_structures', {}).get('canonical_smiles'),
                    'inchi': data.get('molecule_structures', {}).get('standard_inchi'),
                    'inchi_key': data.get('molecule_structures', {}).get('standard_inchi_key'),
                    # Molecular properties
                    'alogp': data.get('molecule_properties', {}).get('alogp'),
                    'hba': data.get('molecule_properties', {}).get('hba'),  # H-bond acceptors
                    'hbd': data.get('molecule_properties', {}).get('hbd'),  # H-bond donors
                    'psa': data.get('molecule_properties', {}).get('psa'),  # Polar surface area
                    'rtb': data.get('molecule_properties', {}).get('rtb'),  # Rotatable bonds
                    'num_ro5_violations': data.get('molecule_properties', {}).get('num_ro5_violations'),
                    # Additional data
                    'synonyms': data.get('molecule_synonyms', [])[:10],
                }
        except Exception as e:
            logger.error(f"Failed to fetch molecule {chembl_id}: {e}")
        return None

    def _fetch_activities(self, chembl_id: str) -> List[Dict]:
        """Fetch bioactivity data for compound"""
        url = f"{self.base_url}/activity.json"
        params = {
            'molecule_chembl_id': chembl_id,
            'limit': 100,  # Get up to 100 activities
        }

        try:
            data = self._make_request(url, params=params)
            if 'activities' in data:
                activities = []
                for activity in data['activities']:
                    activities.append({
                        'activity_id': activity.get('activity_id'),
                        'assay_chembl_id': activity.get('assay_chembl_id'),
                        'target_chembl_id': activity.get('target_chembl_id'),
                        'target_pref_name': activity.get('target_pref_name'),
                        'target_organism': activity.get('target_organism'),
                        'standard_type': activity.get('standard_type'),  # IC50, EC50, Ki, etc.
                        'standard_value': activity.get('standard_value'),
                        'standard_units': activity.get('standard_units'),
                        'standard_relation': activity.get('standard_relation'),
                        'activity_comment': activity.get('activity_comment'),
                    })
                return activities
        except Exception as e:
            logger.debug(f"No activities for {chembl_id}: {e}")
        return []

    def _fetch_mechanisms(self, chembl_id: str) -> List[Dict]:
        """Fetch mechanism of action data"""
        url = f"{self.base_url}/mechanism.json"
        params = {
            'molecule_chembl_id': chembl_id,
        }

        try:
            data = self._make_request(url, params=params)
            if 'mechanisms' in data:
                mechanisms = []
                for mech in data['mechanisms']:
                    mechanisms.append({
                        'mechanism_of_action': mech.get('mechanism_of_action'),
                        'target_chembl_id': mech.get('target_chembl_id'),
                        'action_type': mech.get('action_type'),
                        'mechanism_comment': mech.get('mechanism_comment'),
                    })
                return mechanisms
        except Exception as e:
            logger.debug(f"No mechanisms for {chembl_id}: {e}")
        return []

    def _extract_drug_data(self, molecule: Dict) -> Optional[Dict]:
        """Extract drug-specific data if applicable"""
        max_phase = molecule.get('max_phase', 0)
        # Convert to int if string
        try:
            max_phase = int(max_phase) if max_phase is not None else 0
        except (ValueError, TypeError):
            max_phase = 0

        if max_phase > 0:
            return {
                'max_phase': max_phase,
                'phase_description': self._get_phase_description(max_phase),
                'is_approved': max_phase == 4,
                'therapeutic': molecule.get('therapeutic_flag', False),
            }
        return None

    def _get_phase_description(self, phase: int) -> str:
        """Get clinical trial phase description"""
        phases = {
            0: "Preclinical",
            1: "Phase I - Safety testing in healthy volunteers",
            2: "Phase II - Efficacy and safety in patients",
            3: "Phase III - Large-scale efficacy and safety",
            4: "Approved - FDA/EMA approved drug",
        }
        return phases.get(phase, "Unknown")

    def search_by_name(self, name: str, limit: int = 10) -> List[str]:
        """
        Search compounds by name

        Args:
            name: Compound name (e.g., "aspirin", "ibuprofen")
            limit: Maximum number of results

        Returns:
            List of ChEMBL IDs matching the name
        """
        url = f"{self.base_url}/molecule.json"
        params = {
            'pref_name__icontains': name,
            'limit': limit,
        }

        try:
            data = self._make_request(url, params=params)
            if 'molecules' in data:
                return [mol['molecule_chembl_id'] for mol in data['molecules']]
        except Exception as e:
            logger.error(f"Search failed for '{name}': {e}")
        return []

    def search_by_smiles(self, smiles: str, similarity: int = 70) -> List[str]:
        """
        Search compounds by SMILES similarity

        Args:
            smiles: SMILES string
            similarity: Similarity threshold (0-100)

        Returns:
            List of similar compound ChEMBL IDs
        """
        url = f"{self.base_url}/similarity/{smiles}/{similarity}.json"

        try:
            data = self._make_request(url)
            if 'molecules' in data:
                return [mol['molecule_chembl_id'] for mol in data['molecules']]
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
        return []

    def fetch_approved_drugs(self, limit: int = 100, offset: int = 0) -> List[str]:
        """
        Fetch FDA/EMA approved drugs (Phase 4)

        Args:
            limit: Maximum number of compounds
            offset: Offset for pagination (default 0)

        Returns:
            List of ChEMBL IDs for approved drugs
        """
        url = f"{self.base_url}/molecule.json"
        params = {
            'max_phase': 4,  # Approved drugs
            'limit': limit,
            'offset': offset,
        }

        try:
            data = self._make_request(url, params=params)
            if 'molecules' in data:
                return [mol['molecule_chembl_id'] for mol in data['molecules']]
        except Exception as e:
            logger.error(f"Failed to fetch approved drugs: {e}")
        return []

    def fetch_by_target(self, target_chembl_id: str, limit: int = 100) -> List[str]:
        """
        Fetch compounds by target protein

        Args:
            target_chembl_id: ChEMBL target ID (e.g., "CHEMBL204" for COX-2)
            limit: Maximum number of compounds

        Returns:
            List of ChEMBL IDs for compounds targeting this protein
        """
        url = f"{self.base_url}/activity.json"
        params = {
            'target_chembl_id': target_chembl_id,
            'limit': limit,
        }

        try:
            data = self._make_request(url, params=params)
            if 'activities' in data:
                # Extract unique molecule IDs
                molecule_ids = set()
                for activity in data['activities']:
                    if 'molecule_chembl_id' in activity:
                        molecule_ids.add(activity['molecule_chembl_id'])
                return list(molecule_ids)
        except Exception as e:
            logger.error(f"Failed to fetch compounds for target {target_chembl_id}: {e}")
        return []

    def fetch_natural_products(self, limit: int = 100, offset: int = 0) -> List[str]:
        """
        Fetch natural products

        Args:
            limit: Maximum number of compounds
            offset: Offset for pagination (default 0)

        Returns:
            List of ChEMBL IDs for natural products
        """
        url = f"{self.base_url}/molecule.json"
        params = {
            'natural_product': 1,  # Natural products flag
            'limit': limit,
            'offset': offset,
        }

        try:
            data = self._make_request(url, params=params)
            if 'molecules' in data:
                return [mol['molecule_chembl_id'] for mol in data['molecules']]
        except Exception as e:
            logger.error(f"Failed to fetch natural products: {e}")
        return []


def main():
    """Demo ChEMBL fetcher"""
    print("="*70)
    print("ChEMBL Data Fetcher Demo")
    print("="*70)

    fetcher = ChEMBLFetcher()

    # Example 1: Fetch aspirin
    print("\n1. Fetching Aspirin (CHEMBL25)...")
    aspirin = fetcher.fetch_compound("CHEMBL25")
    if aspirin:
        mol = aspirin['molecule']
        print(f"   Name: {mol['pref_name']}")
        print(f"   Formula: {mol['molecular_formula']}")
        print(f"   MW: {mol['molecular_weight']:.2f}")
        print(f"   Clinical Phase: {mol['max_phase']} - {fetcher._get_phase_description(mol['max_phase'])}")
        print(f"   Bioactivities: {aspirin['activity_count']}")
        if aspirin['mechanisms']:
            print(f"   Mechanism: {aspirin['mechanisms'][0]['mechanism_of_action']}")

    # Example 2: Search by name
    print("\n2. Searching for 'ibuprofen'...")
    chembl_ids = fetcher.search_by_name("ibuprofen", limit=3)
    print(f"   Found {len(chembl_ids)} compounds: {chembl_ids}")

    # Example 3: Fetch approved drugs
    print("\n3. Fetching approved drugs...")
    approved = fetcher.fetch_approved_drugs(limit=10)
    print(f"   Found {len(approved)} approved drugs")

    # Example 4: Fetch natural products
    print("\n4. Fetching natural products...")
    natural = fetcher.fetch_natural_products(limit=10)
    print(f"   Found {len(natural)} natural products")

    # Print statistics
    fetcher.print_stats()


if __name__ == "__main__":
    main()
