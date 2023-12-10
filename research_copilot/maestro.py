"""Maestro module."""

import json
import glob
from datetime import datetime
from rdflib import Graph

g = Graph()

def load_knowledge_assets(path):
    """Load knowledge assets into local cache."""
    json_files = glob.glob(f'{path}/**/*.json', recursive=True)
    for file in json_files:
        print(f'Loading {file}')
        with open(file, 'r', encoding="utf-8") as file:
            data = json.load(file)
            jsonld_data = {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "itemListElement": [{'public': {k: v for k, v in d['public'].items() if k != '@context'}} for d in data] # remove @context from assets
            }
            g.parse(data=jsonld_data, format='json-ld')

def get_answer(sparql_query):
    """Performs SPARQL query."""
    results_list = []
    try:
        result = g.query(sparql_query)
        for row in result:
            item = {}
            for var, val in zip(result.vars, row):
                item[var] = str(val)
            results_list.append(item)
    except Exception as e:
        print('An exception occurred:', e)

    return results_list

def log_to_influxdb(client, request_data, response_data, is_empty):
    """Log copilot request and response."""
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    json_body = [
        {
            "measurement": "api_logs",
            "time": current_time,
            "fields": {
                "request": str(request_data),
                "response": str(response_data),
                "is_empty": is_empty
            }
        }
    ]
    client.write_points(json_body)
