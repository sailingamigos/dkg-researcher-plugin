"""DKG client module."""

import os
import json
from helper import normalize_path # pylint: disable=import-error

def publish_assets(path, data):
    """
    Publish assets in JSON-LD format.

    Args:
        path (str): The path where the JSON-LD file will be saved.
        data (dict): A dictionary containing the data to be saved in the JSON-LD file.
    """
    # Ensure the directory structure exists for the given path
    if not os.path.exists(os.path.dirname(normalize_path(path + '.json'))):
        os.makedirs(os.path.dirname(normalize_path(path + '.json')))
    
    # Write data to the JSON-LD file
    with open(normalize_path(path + '.json'), 'w', encoding='utf-8') as file:
        json.dump([{'public': data}], file, indent=4)
