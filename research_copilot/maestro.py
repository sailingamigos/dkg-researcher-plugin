"""Maestro module."""

import os
import json
import glob
import numpy as np
from datetime import datetime
from rdflib import Graph
from dotenv import load_dotenv
from quart import request, jsonify, redirect
from dkg import DKG
from dkg.providers import BlockchainProvider, NodeHTTPProvider
from ai_cortex import kmeans_algorithm, linear_regression_algorithm

load_dotenv()

dkg_graph = None
local_graph = Graph()

def connect_to_otnode():
    """Initialize the DKG endpoint."""
    global dkg_graph
    node_provider = NodeHTTPProvider(os.getenv('DKG_ENDPOINT'))
    dkg_graph = DKG(node_provider, None)
    print(f'DKG: {dkg_graph.node.info}')


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
            local_graph.parse(data=jsonld_data, format='json-ld')

def query_dkg(sparql_query):
    """Performs SPARQL query."""
    try:
        dkg_result = dkg_graph.graph.query(sparql_query, repository="publicCurrent")
        if dkg_result:
            return dkg_result
    except Exception as e:
        print(f'DKG query failed: {e}')
    return None

def query_local_graph(sparql_query):
    """Performs SPARQL query."""
    try:
        graph_result = []
        result = local_graph.query(sparql_query)
        if result:
            for row in result:
                item = {}
                for var, val in zip(result.vars, row):
                    item[var] = str(val)
                graph_result.append(item)
        if graph_result:
            return graph_result
    except Exception as e:
        print(f'Local graph query failed: {e}')
    return None

def get_answer(sparql_query):
    """Performs SPARQL query using a chain of callbacks."""
    for query_function in [query_local_graph]: # query_dkg
        result = query_function(sparql_query)
        if result is not None:
            return result
    return []

def perform_kmeans(data):
    """Perform kmeans"""
    X = np.array(data['X']).reshape(-1, 1)
    k = data['k']
    return kmeans_algorithm(X, k)

def perform_regression(data):
    """Perform logistic regression"""
    X = np.array(data['X']).reshape(-1, 1)
    y = np.array(data['y'])
    predict_data = np.array(data['predict_data'])
    return linear_regression_algorithm(X,y,predict_data)

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
