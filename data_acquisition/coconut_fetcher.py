#!/usr/bin/env python3
"""
COCONUT Natural Products Fetcher
Fetch natural product data from COCONUT database (400K+ natural products)
API Docs: https://coconut.naturalproducts.net/
"""

import logging
from typing import Dict, List, Optional
from .base_fetcher import BaseFetcher, FetcherConfig

logger = logging.getLogger(__name__)


class COCONUTFetcher(BaseFetcher):
    """
    Fetch natural product data from COCONUT database

    Data Available:
    - Natural products: 400K+
    - Source organisms: 50K+
    - Geographic origins
    - Traditional medicinal uses
    - Biosynthetic pathways
    - Taxonomic information
    - Chemical diversity
    """

    @property
    def source_name(self) -> str:
        return "coconut"

    @property
    def base_url(self) -> str:
        return "https://coconut.naturalproducts.net/api/v1"

    def fetch_compound(self, coconut_id: str) -> Optional[Dict]:
        """
        Fetch natural product data by COCONUT ID

        Args:
            coconut_id: COCONUT identifier (e.g., "CNP0123456")

        Returns:
            Natural product data with organism source, traditional uses, etc.
        """
        cache_key = f"np_{coconut_id}"
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached

        try:
            # Fetch natural product data
            np_data = self._fetch_natural_product(coconut_id)
            if not np_data:
                return None

            # Compile compound data
            compound_data = {
                'source': 'coconut',
                'coconut_id': coconut_id,
                'name': np_data.get('name'),
                'iupac_name': np_data.get('iupac_name'),
                'smiles': np_data.get('smiles'),
                'inchi': np_data.get('inchi'),
                'inchi_key': np_data.get('inchikey'),
                'molecular_formula': np_data.get('molecular_formula'),
                'molecular_weight': np_data.get('molecular_weight'),
                # Natural product specific
                'organism_sources': np_data.get('organism_sources', []),
                'geographic_origins': np_data.get('geographic_origins', []),
                'traditional_uses': np_data.get('traditional_uses', []),
                'natural_product_class': np_data.get('np_class'),
                'biosynthetic_pathway': np_data.get('pathway'),
                'taxonomy': np_data.get('taxonomy', {}),
                # Chemical properties
                'properties': {
                    'logp': np_data.get('alogp'),
                    'tpsa': np_data.get('tpsa'),
                    'h_bond_donors': np_data.get('hbd'),
                    'h_bond_acceptors': np_data.get('hba'),
                    'rotatable_bonds': np_data.get('rotatable_bonds'),
                    'num_rings': np_data.get('num_rings'),
                    'aromatic_rings': np_data.get('aromatic_rings'),
                },
            }

            self._save_to_cache(cache_key, compound_data)
            return compound_data

        except Exception as e:
            logger.error(f"Failed to fetch COCONUT ID {coconut_id}: {e}")
            return None

    def _fetch_natural_product(self, coconut_id: str) -> Optional[Dict]:
        """Fetch natural product core data"""
        url = f"{self.base_url}/compound/{coconut_id}"

        try:
            data = self._make_request(url)
            return data
        except Exception as e:
            logger.error(f"Failed to fetch natural product {coconut_id}: {e}")
        return None

    def search_by_name(self, name: str, limit: int = 10) -> List[str]:
        """
        Search natural products by name

        Args:
            name: Natural product name
            limit: Maximum number of results

        Returns:
            List of COCONUT IDs matching the name
        """
        url = f"{self.base_url}/search/name"
        params = {
            'query': name,
            'limit': limit,
        }

        try:
            data = self._make_request(url, params=params)
            if isinstance(data, list):
                return [item.get('coconut_id') for item in data if 'coconut_id' in item]
        except Exception as e:
            logger.error(f"Search failed for '{name}': {e}")
        return []

    def search_by_organism(self, organism: str, limit: int = 100) -> List[str]:
        """
        Search natural products by source organism

        Args:
            organism: Organism name (e.g., "Cannabis sativa", "Streptomyces")
            limit: Maximum number of results

        Returns:
            List of COCONUT IDs for natural products from this organism
        """
        url = f"{self.base_url}/search/organism"
        params = {
            'query': organism,
            'limit': limit,
        }

        try:
            data = self._make_request(url, params=params)
            if isinstance(data, list):
                return [item.get('coconut_id') for item in data if 'coconut_id' in item]
        except Exception as e:
            logger.error(f"Search failed for organism '{organism}': {e}")
        return []

    def fetch_by_class(self, np_class: str, limit: int = 100) -> List[str]:
        """
        Fetch natural products by chemical class

        Args:
            np_class: Natural product class (e.g., "alkaloid", "terpenoid", "flavonoid")
            limit: Maximum number of results

        Returns:
            List of COCONUT IDs for this class
        """
        url = f"{self.base_url}/search/class"
        params = {
            'query': np_class,
            'limit': limit,
        }

        try:
            data = self._make_request(url, params=params)
            if isinstance(data, list):
                return [item.get('coconut_id') for item in data if 'coconut_id' in item]
        except Exception as e:
            logger.error(f"Search failed for class '{np_class}': {e}")
        return []

    def fetch_alkaloids(self, limit: int = 100) -> List[str]:
        """Fetch alkaloids (nitrogen-containing natural products)"""
        return self.fetch_by_class("alkaloid", limit)

    def fetch_terpenoids(self, limit: int = 100) -> List[str]:
        """Fetch terpenoids (isoprenoid-derived compounds)"""
        return self.fetch_by_class("terpenoid", limit)

    def fetch_polyketides(self, limit: int = 100) -> List[str]:
        """Fetch polyketides (fatty acid-derived metabolites)"""
        return self.fetch_by_class("polyketide", limit)

    def fetch_flavonoids(self, limit: int = 100) -> List[str]:
        """Fetch flavonoids (plant phenolic compounds)"""
        return self.fetch_by_class("flavonoid", limit)

    def fetch_plant_metabolites(self, limit: int = 100) -> List[str]:
        """
        Fetch plant-derived natural products

        Returns:
            List of COCONUT IDs for plant metabolites
        """
        # Common plant genera for natural products
        plants = [
            "Cannabis",
            "Curcuma",
            "Salvia",
            "Artemisia",
            "Taxus",
            "Catharanthus",
        ]

        all_ids = set()
        for plant in plants:
            ids = self.search_by_organism(plant, limit=20)
            all_ids.update(ids)
            if len(all_ids) >= limit:
                break

        return list(all_ids)[:limit]

    def fetch_fungal_metabolites(self, limit: int = 100) -> List[str]:
        """
        Fetch fungus-derived natural products

        Returns:
            List of COCONUT IDs for fungal metabolites
        """
        fungi = [
            "Penicillium",
            "Aspergillus",
            "Fusarium",
            "Amanita",
        ]

        all_ids = set()
        for fungus in fungi:
            ids = self.search_by_organism(fungus, limit=25)
            all_ids.update(ids)
            if len(all_ids) >= limit:
                break

        return list(all_ids)[:limit]

    def fetch_bacterial_metabolites(self, limit: int = 100) -> List[str]:
        """
        Fetch bacteria-derived natural products

        Returns:
            List of COCONUT IDs for bacterial metabolites
        """
        bacteria = [
            "Streptomyces",
            "Bacillus",
            "Pseudomonas",
        ]

        all_ids = set()
        for bacterium in bacteria:
            ids = self.search_by_organism(bacterium, limit=30)
            all_ids.update(ids)
            if len(all_ids) >= limit:
                break

        return list(all_ids)[:limit]


def main():
    """Demo COCONUT fetcher"""
    print("="*70)
    print("COCONUT Natural Products Fetcher Demo")
    print("="*70)

    fetcher = COCONUTFetcher()

    # Note: COCONUT API may have rate limits or different endpoints
    # This is a template - actual implementation may need adjustment
    # based on current API specification

    print("\n1. Fetching alkaloids...")
    alkaloids = fetcher.fetch_alkaloids(limit=5)
    print(f"   Found {len(alkaloids)} alkaloid IDs")

    print("\n2. Fetching plant metabolites...")
    plants = fetcher.fetch_plant_metabolites(limit=10)
    print(f"   Found {len(plants)} plant metabolite IDs")

    print("\n3. Fetching fungal metabolites...")
    fungi = fetcher.fetch_fungal_metabolites(limit=10)
    print(f"   Found {len(fungi)} fungal metabolite IDs")

    # Print statistics
    fetcher.print_stats()


if __name__ == "__main__":
    main()
