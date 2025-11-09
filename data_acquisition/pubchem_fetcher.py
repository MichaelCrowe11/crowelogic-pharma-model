#!/usr/bin/env python3
"""
PubChem Data Fetcher
Fetch compound data from PubChem (150M+ compounds)
API Docs: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
"""

import logging
from typing import Dict, List, Optional
from .base_fetcher import BaseFetcher, FetcherConfig

logger = logging.getLogger(__name__)


class PubChemFetcher(BaseFetcher):
    """
    Fetch compound data from PubChem database

    Data Available:
    - Molecular properties (MW, logP, TPSA, etc.)
    - 2D/3D structures (SMILES, InChI)
    - Bioactivity data
    - Synonyms and names
    - Patent information
    - Literature references
    """

    @property
    def source_name(self) -> str:
        return "pubchem"

    @property
    def base_url(self) -> str:
        return "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def fetch_compound(self, cid: str) -> Optional[Dict]:
        """
        Fetch compound data by PubChem CID

        Args:
            cid: PubChem Compound ID (e.g., "2244" for aspirin)

        Returns:
            Compound data with properties, structure, and metadata
        """
        cache_key = f"compound_{cid}"
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached

        try:
            # Fetch properties
            properties = self._fetch_properties(cid)
            if not properties:
                return None

            # Fetch synonyms
            synonyms = self._fetch_synonyms(cid)

            # Fetch bioactivity (if available)
            bioactivity = self._fetch_bioactivity(cid)

            # Compile compound data
            compound_data = {
                'source': 'pubchem',
                'cid': cid,
                'properties': properties,
                'synonyms': synonyms[:10],  # Top 10 synonyms
                'bioactivity_count': len(bioactivity) if bioactivity else 0,
                'bioactivity': bioactivity[:5] if bioactivity else [],  # Sample
            }

            self._save_to_cache(cache_key, compound_data)
            return compound_data

        except Exception as e:
            logger.error(f"Failed to fetch PubChem CID {cid}: {e}")
            return None

    def _fetch_properties(self, cid: str) -> Optional[Dict]:
        """Fetch molecular properties"""
        url = f"{self.base_url}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,Complexity,Charge/JSON"

        try:
            data = self._make_request(url)
            if 'PropertyTable' in data and 'Properties' in data['PropertyTable']:
                props = data['PropertyTable']['Properties'][0]
                return {
                    'molecular_formula': props.get('MolecularFormula'),
                    'molecular_weight': props.get('MolecularWeight'),
                    'canonical_smiles': props.get('CanonicalSMILES'),
                    'isomeric_smiles': props.get('IsomericSMILES'),
                    'inchi': props.get('InChI'),
                    'inchi_key': props.get('InChIKey'),
                    'iupac_name': props.get('IUPACName'),
                    'logp': props.get('XLogP'),
                    'tpsa': props.get('TPSA'),
                    'h_bond_donors': props.get('HBondDonorCount'),
                    'h_bond_acceptors': props.get('HBondAcceptorCount'),
                    'rotatable_bonds': props.get('RotatableBondCount'),
                    'complexity': props.get('Complexity'),
                    'charge': props.get('Charge'),
                }
        except Exception as e:
            logger.error(f"Failed to fetch properties for CID {cid}: {e}")
        return None

    def _fetch_synonyms(self, cid: str) -> List[str]:
        """Fetch compound synonyms/names"""
        url = f"{self.base_url}/compound/cid/{cid}/synonyms/JSON"

        try:
            data = self._make_request(url)
            if 'InformationList' in data:
                info = data['InformationList']['Information'][0]
                return info.get('Synonym', [])
        except Exception as e:
            logger.debug(f"No synonyms for CID {cid}: {e}")
        return []

    def _fetch_bioactivity(self, cid: str) -> List[Dict]:
        """Fetch bioactivity data"""
        url = f"{self.base_url}/compound/cid/{cid}/assaysummary/JSON"

        try:
            data = self._make_request(url)
            if 'Table' in data and 'Row' in data['Table']:
                return data['Table']['Row']
        except Exception as e:
            logger.debug(f"No bioactivity for CID {cid}: {e}")
        return []

    def search_by_name(self, name: str, limit: int = 10) -> List[str]:
        """
        Search compounds by name

        Args:
            name: Compound name (e.g., "aspirin", "caffeine")
            limit: Maximum number of results

        Returns:
            List of CIDs matching the name
        """
        url = f"{self.base_url}/compound/name/{name}/cids/JSON"

        try:
            data = self._make_request(url)
            if 'IdentifierList' in data:
                cids = data['IdentifierList']['CID']
                return [str(cid) for cid in cids[:limit]]
        except Exception as e:
            logger.error(f"Search failed for '{name}': {e}")
        return []

    def search_by_smiles(self, smiles: str, similarity: float = 0.9) -> List[str]:
        """
        Search compounds by SMILES similarity

        Args:
            smiles: SMILES string
            similarity: Similarity threshold (0.0-1.0)

        Returns:
            List of similar compound CIDs
        """
        # PubChem similarity search
        url = f"{self.base_url}/compound/fastsimilarity_2d/smiles/{smiles}/cids/JSON"

        params = {
            'Threshold': int(similarity * 100),
            'MaxRecords': 100
        }

        try:
            data = self._make_request(url, params=params)
            if 'IdentifierList' in data:
                return [str(cid) for cid in data['IdentifierList']['CID']]
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
        return []

    def fetch_drug_compounds(self, limit: int = 1000) -> List[str]:
        """
        Fetch FDA-approved drug compounds

        Args:
            limit: Maximum number of compounds

        Returns:
            List of CIDs for drug compounds
        """
        # Search for FDA-approved drugs
        categories = [
            "FDA approved drug",
            "pharmaceutical",
            "therapeutic",
        ]

        all_cids = set()
        for category in categories:
            cids = self.search_by_name(category, limit=500)
            all_cids.update(cids)
            if len(all_cids) >= limit:
                break

        return list(all_cids)[:limit]

    def fetch_natural_products(self, limit: int = 1000) -> List[str]:
        """
        Fetch natural product compounds

        Args:
            limit: Maximum number of compounds

        Returns:
            List of CIDs for natural products
        """
        categories = [
            "natural product",
            "plant metabolite",
            "fungal metabolite",
            "bacterial metabolite",
        ]

        all_cids = set()
        for category in categories:
            cids = self.search_by_name(category, limit=300)
            all_cids.update(cids)
            if len(all_cids) >= limit:
                break

        return list(all_cids)[:limit]


def main():
    """Demo PubChem fetcher"""
    print("="*70)
    print("PubChem Data Fetcher Demo")
    print("="*70)

    fetcher = PubChemFetcher()

    # Example 1: Fetch aspirin
    print("\n1. Fetching Aspirin (CID: 2244)...")
    aspirin = fetcher.fetch_compound("2244")
    if aspirin:
        print(f"   Name: {aspirin['synonyms'][0]}")
        print(f"   Formula: {aspirin['properties']['molecular_formula']}")
        print(f"   MW: {aspirin['properties']['molecular_weight']:.2f}")
        print(f"   logP: {aspirin['properties']['logp']}")
        print(f"   SMILES: {aspirin['properties']['canonical_smiles']}")

    # Example 2: Search by name
    print("\n2. Searching for 'caffeine'...")
    cids = fetcher.search_by_name("caffeine", limit=5)
    print(f"   Found {len(cids)} compounds: {cids}")

    # Example 3: Fetch drug compounds
    print("\n3. Fetching FDA-approved drugs...")
    drug_cids = fetcher.fetch_drug_compounds(limit=10)
    print(f"   Found {len(drug_cids)} drug compounds")

    # Print statistics
    fetcher.print_stats()


if __name__ == "__main__":
    main()
