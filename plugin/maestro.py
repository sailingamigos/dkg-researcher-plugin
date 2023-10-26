"""Maestro module."""

import json
from datetime import datetime
from rdflib import Graph

g = Graph()

def load_data (path):
    """Loads assets from cache file."""
    with open(path, 'r', encoding="utf-8") as file:
        g.parse(file, format='json-ld')

def get_answer (payload):
    """Performs SPARQL query."""
    results_list = []
    try:
        result = g.query(payload['sparqlQuery'])
        for row in result:
            item = {}
            for var, val in zip(result.vars, row):
                item[var] = str(val)
            results_list.append(item)
    except:
        print("An exception occurred")

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
