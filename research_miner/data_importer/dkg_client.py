"""DKG client."""

import os
import json
from helper import normalize_path # pylint: disable=import-error

def publish_assets(path, data):
    """Publish assets to the DKG"""
    # TBD

    if not os.path.exists(os.path.dirname(normalize_path(path + '.json'))):
        os.makedirs(os.path.dirname(normalize_path(path + '.json')))
    with open(normalize_path(path + '.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
