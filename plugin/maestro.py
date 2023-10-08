"""Maestro module."""

import json
from rdflib import Graph

g = Graph()

def load_data (path):
    """Loads assets from cache file."""
    with open(path, 'r', encoding="utf-8") as file:
        g.parse(file, format='json-ld')

def get_answer (payload):
    """Performs SPARQL query."""
    result = g.query(payload['sparqlQuery'])
    results_list = []
    for row in result:
        item = {}
        for var, val in zip(result.vars, row):
            item[var] = str(val)
        results_list.append(item)

    return results_list
