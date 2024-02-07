"""Maestro module."""

import os
import json
import glob
import requests
from datetime import datetime
import numpy as np # pylint: disable=import-error
from rdflib import Graph # pylint: disable=import-error
from dotenv import load_dotenv # pylint: disable=import-error
from dkg import DKG # pylint: disable=import-error
from dkg.providers import NodeHTTPProvider # pylint: disable=import-error
from ai_cortex import kmeans_algorithm, linear_regression_algorithm, vector_search_algorithm

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
        with open(file, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)[0]['public']
            jsonld_data = {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "itemListElement": [
                    {k: v for k, v in d.items() if k != '@context'} for d in data
                ]  # Remove '@context' from assets
            }
            local_graph.parse(data=jsonld_data, format='json-ld')

def query_dkg(sparql_query):
    """Performs SPARQL query."""
    try:
        payload = {
        'query': sparql_query,
        'queryType': 'SELECT',
        'responseFormat': 'application/json'
        }
        headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': f'Basic {os.getenv("NOS_AUTH_BASIC")} Bearer {os.getenv("NOS_AUTH_BEARER")}',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        dkg_result = requests.request("POST", os.getenv('NOS_ENDPOINT'), headers=headers, data=payload, timeout=30)

        # dkg_result = dkg_graph.graph.query(sparql_query, repository="publicHistory")
        if dkg_result:
            return json.loads(dkg_result.text)['queryResult']
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
                    item[var.toPython()] = str(val)
                graph_result.append(item)
        if graph_result:
            return graph_result
    except Exception as e:
        print(f'Local graph query failed: {e}')
    return None

def get_answer(payload):
    """Performs SPARQL query using a chain of callbacks."""
    repository = payload['repository']
    primary_sparql_query = payload['scholarlyArticleSparqlQuery']
    secondary_sparql_query = payload['arxivSparqlQuery']

    if repository == 1:
        sparql_queries = [primary_sparql_query]
    elif repository == 2:
        sparql_queries = [secondary_sparql_query]
    else:
        sparql_queries = [primary_sparql_query, secondary_sparql_query]

    response = []

    for query_function in [query_dkg, query_local_graph]:
        for sparql_query in sparql_queries:
            result = query_function(sparql_query)
            if result is not None:
                graph_name = 'DKG' if query_function.__name__ == 'query_dkg' else 'Local'
                repository_name = 'SemanticScholar' if sparql_query == primary_sparql_query else 'Arxiv'
                response.append((graph_name, repository_name, result))

    return response

def perform_kmeans(data):
    """Perform k-means clustering."""
    X = data['X']
    k = data['k']
    return kmeans_algorithm(X, k)

def perform_regression(data):
    """Perform linear regression."""
    X = np.array(data['X']).reshape(-1, 1)
    y = np.array(data['y'])
    predict_data = np.array(data['predict_data']).reshape(-1, 1)
    return linear_regression_algorithm(X, y, predict_data)

def perform_vector_search(data):
    """Perform vector search."""
    question = data['question']
    response = get_answer({
        'repository': 1,
        'scholarlyArticleSparqlQuery': """
            PREFIX  :     <http://schema.org/>
            SELECT  ?title ?abstract ?embedding
            WHERE
            {   
                ?paper      a           :ScholarlyArticle ;
                            :embedding  ?embedding ;
                            :title      ?title ;
                            :abstract   ?abstract .
                FILTER (?embedding != 'None')
            }
        """,
        'arxivSparqlQuery': ''
    })
    (graph, repository, result) = response[0]
    embedding_field_name = 'embedding' if graph == 'DKG' else '?embedding'
    vectors = [json.loads(obj[embedding_field_name]) for obj in result]
    if graph == 'DKG':
        vectors = [json.loads(obj) for obj in vectors]
    sorted_indices = vector_search_algorithm(question, vectors)

    n = 3
    top_n_papers = [result[i] for i in sorted_indices[:n]]
    top_n_papers = [{k: v for k, v in paper.items() if k != embedding_field_name} for paper in top_n_papers]

    return (graph, repository, top_n_papers)

def log_to_influxdb(client, request_data, response_data, is_empty):
    """Log API request and response to InfluxDB."""
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
