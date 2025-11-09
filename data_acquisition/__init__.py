"""
Data Acquisition Module
Multi-source pharmaceutical data fetchers
"""

from .base_fetcher import BaseFetcher, FetcherConfig
from .pubchem_fetcher import PubChemFetcher

__all__ = [
    'BaseFetcher',
    'FetcherConfig',
    'PubChemFetcher',
]
