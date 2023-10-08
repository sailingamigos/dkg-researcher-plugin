"""Assets bot generator module."""

import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def publish_assets (data, path):
    """Save assets to the file."""
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
