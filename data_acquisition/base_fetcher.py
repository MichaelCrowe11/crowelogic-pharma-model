#!/usr/bin/env python3
"""
Base Data Fetcher
Abstract class for all data source fetchers with caching, rate limiting, and retry logic
"""

import time
import requests
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
from functools import wraps
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FetcherConfig:
    """Configuration for data fetchers"""
    cache_dir: Path = Path("./cache")
    rate_limit_calls: int = 5  # calls per second
    max_retries: int = 3
    timeout: int = 30
    batch_size: int = 100


class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_second: int):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = defaultdict(float)

    def wait(self, key: str = "default"):
        """Wait if necessary to respect rate limit"""
        elapsed = time.time() - self.last_call[key]
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call[key] = time.time()


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator


class BaseFetcher(ABC):
    """
    Abstract base class for all data source fetchers

    Provides:
    - Caching system
    - Rate limiting
    - Retry logic
    - Error handling
    - Batch processing
    """

    def __init__(self, config: Optional[FetcherConfig] = None):
        self.config = config or FetcherConfig()
        self.cache_dir = self.config.cache_dir / self.source_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.rate_limiter = RateLimiter(self.config.rate_limit_calls)
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)

        self.stats = {
            'fetched': 0,
            'cached': 0,
            'failed': 0,
            'total_time': 0.0
        }

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the data source (e.g., 'pubchem', 'chembl')"""
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Base URL for the API"""
        pass

    @property
    def default_headers(self) -> Dict[str, str]:
        """Default headers for requests"""
        return {
            'User-Agent': 'CroweLogic-Pharma/2.0 (Educational Research)',
            'Accept': 'application/json',
        }

    def _get_cache_path(self, cache_key: str) -> Path:
        """Generate cache file path from key"""
        hash_key = hashlib.md5(cache_key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.json"

    def _load_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Load data from cache if available"""
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    self.stats['cached'] += 1
                    logger.debug(f"Loaded from cache: {cache_key}")
                    return data
            except Exception as e:
                logger.warning(f"Cache read failed for {cache_key}: {e}")
        return None

    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache"""
        cache_path = self._get_cache_path(cache_key)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved to cache: {cache_key}")
        except Exception as e:
            logger.warning(f"Cache write failed for {cache_key}: {e}")

    @retry_on_failure(max_retries=3)
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request with rate limiting and error handling"""
        self.rate_limiter.wait(self.source_name)

        start_time = time.time()
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()

            self.stats['fetched'] += 1
            self.stats['total_time'] += time.time() - start_time

            return response.json()

        except requests.exceptions.RequestException as e:
            self.stats['failed'] += 1
            logger.error(f"Request failed for {url}: {e}")
            raise

    @abstractmethod
    def fetch_compound(self, compound_id: str) -> Optional[Dict]:
        """Fetch data for a single compound"""
        pass

    def fetch_compounds_batch(self, compound_ids: List[str]) -> List[Dict]:
        """Fetch data for multiple compounds"""
        results = []
        for compound_id in compound_ids:
            try:
                data = self.fetch_compound(compound_id)
                if data:
                    results.append(data)
            except Exception as e:
                logger.error(f"Failed to fetch {compound_id}: {e}")
                continue
        return results

    def search(self, query: str, limit: int = 100) -> List[Dict]:
        """Search for compounds matching query"""
        raise NotImplementedError(f"{self.source_name} search not implemented")

    def get_stats(self) -> Dict[str, Any]:
        """Get fetcher statistics"""
        return {
            **self.stats,
            'cache_size_mb': sum(
                f.stat().st_size for f in self.cache_dir.glob('*.json')
            ) / (1024 * 1024),
            'avg_fetch_time': (
                self.stats['total_time'] / self.stats['fetched']
                if self.stats['fetched'] > 0 else 0
            )
        }

    def print_stats(self):
        """Print fetcher statistics"""
        stats = self.get_stats()
        print(f"\n{self.source_name.upper()} Fetcher Statistics:")
        print(f"  Fetched: {stats['fetched']}")
        print(f"  Cached: {stats['cached']}")
        print(f"  Failed: {stats['failed']}")
        print(f"  Cache size: {stats['cache_size_mb']:.2f} MB")
        print(f"  Avg fetch time: {stats['avg_fetch_time']:.3f}s")

    def clear_cache(self):
        """Clear all cached data"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Cleared cache for {self.source_name}")
