"""Cache helper module."""

import os
import pickle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def normalize_path(key):
    """Normalize path."""
    key = key.replace(' ', '_')
    return os.path.join(ROOT, 'knowledge_assets', key).lower()

def cache_exists(key):
    """Check if cache exists."""
    return os.path.exists(normalize_path(f'cache/{key}.pkl'))

def get_cache(key):
    """Get cache."""
    cache_file = normalize_path(f'cache/{key}.pkl')
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as file:
            cached_data = pickle.load(file)
            return cached_data

def set_cache(key, value):
    """Set cache."""
    cache_file = normalize_path(f'cache/{key}.pkl')
    if not os.path.exists(os.path.dirname(cache_file)):
        os.makedirs(os.path.dirname(cache_file))
    with open(cache_file, 'wb') as file:
        pickle.dump(value, file)
