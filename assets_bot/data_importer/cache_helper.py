"""Cache helper module."""

import os
import pickle
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def normalize_path (key):
    """Normalize path."""
    key = key.replace(' ', '_')
    return os.path.join(PROJECT_ROOT, 'cache', f'{key}.pkl')

def cache_exists (key):
    """Check if cache exists."""
    return os.path.exists(normalize_path(key))

def get_cache (key):
    """Get cache."""
    cache_file = normalize_path(key)
    if os.path.exists (cache_file):
        with open(cache_file, 'rb') as file:
            cached_data = pickle.load(file)
            return json.loads(cached_data)

def set_cache (key, value):
    """Set cache."""
    cache_file = normalize_path(key)
    with open(cache_file, 'wb') as file:
        pickle.dump(value, file)
