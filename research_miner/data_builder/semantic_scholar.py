"""Semantic scholar builder module."""

import os
import json
import requests
from http.client import HTTPException
from dotenv import load_dotenv # pylint: disable=import-error
from helper import get_cache, set_cache, cache_exists # pylint: disable=import-error

load_dotenv()

def get_papers(repository, topic, limit, offset, cache):
    """Fetch scholarly papers from Semantic Scholar API.

    Args:
        repository (object): The repository object.
        topic (str): The topic or query for fetching papers.
        limit (int): The maximum number of papers to fetch.
        offset (int): The starting point for fetching papers.
        cache (bool): Whether to use cached data if available.

    Returns:
        list: List of scholarly papers data.
        
    Raises:
        HTTPException: If the API request fails.
    """
    cache_path = f'{repository.name}_{topic}/{repository.name}_{topic}_{limit}_{offset}_papers'
    if cache and cache_exists(cache_path):
        return get_cache(cache_path)

    url = 'https://api.semanticscholar.org/graph/v1/paper/search/bulk'
    params = {
        'query': topic,
        'openAccessPdf': 'true',
        'offset': offset,
        'limit': limit,
        'fields': (
            'paperId,corpusId,externalIds,url,title,abstract,venue,publicationVenue,'+
            'year,referenceCount,citationCount,'+
            'isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy,'+
            'publicationTypes,journal,authors'
        )
    }
    headers = {'x-api-key': os.getenv('SEMANTIC_SCHOLAR_API_KEY')}
    response = requests.get(url, params=params, headers=headers, timeout=60)

    if response.status_code == 200:
        if cache:
            set_cache(cache_path, json.loads(response.text)['data'])
        return json.loads(response.text)['data']

    raise HTTPException(f'Failed to fetch data: {response.status_code}')

def get_paper_info(paper_id, cache):
    """Fetch additional information about a scholarly paper.

    Args:
        paper_id (str): The ID of the paper to fetch additional info.
        cache (bool): Whether to use cached data if available.

    Returns:
        dict: Additional information about the paper.
        
    Raises:
        HTTPException: If the API request fails.
    """
    cache_path = f'papers/paper_{paper_id}'
    if cache and cache_exists(cache_path):
        return get_cache(cache_path)
    response = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}',
                params={'fields':('embedding,citations.paperId,citations.title,citations.url')},
                headers={'x-api-key': os.getenv('SEMANTIC_SCHOLAR_API_KEY')},
                timeout=30)

    if response.status_code == 200:
        if cache:
            set_cache(cache_path, response.json())
        return response.json()

    raise HTTPException(f'Failed to fetch additional data: {response.status_code}')

def create_assets(papers, cache):
    """Create knowledge assets from scholarly papers data.

    Args:
        papers (list): List of scholarly papers data.
        cache (bool): Whether to use cached data if available.

    Returns:
        list: List of knowledge assets in ScholarlyArticle format.
    """
    result = []
    for i, input_data in enumerate(papers):
        if not all(input_data.get(field) is not None for field in ['paperId', 'authors']):
            continue
        scholarlyarticle = {
            '@context': 'https://schema.org',
            '@id': 'urn:chatdkg:scientific:' + input_data.get('paperId', None) + '/' + os.getenv('ASSETS_VERSION'),
            '@type': 'ScholarlyArticle',
            'paperId': input_data.get('paperId', None),
            'corpusId': input_data.get('corpusId', None),
            'externalIds': input_data.get('externalIds', None),
            'url': input_data.get('url', None),
            'title': input_data.get('title', None),
            'abstract': input_data.get('abstract', None),
            'publicationTypes': input_data.get('publicationTypes', None),
            'publicationVenue': {
                'id': 'urn:chatdkg:scientific:' + input_data['publicationVenue'].get('id', None) if input_data.get('publicationVenue') else None,
                'name': input_data['publicationVenue'].get('name', None) if input_data.get('publicationVenue') else None,
                'alternate_names': input_data['publicationVenue'].get('alternate_names', None) if input_data.get('publicationVenue') else None,
                'issn': input_data['publicationVenue'].get('issn', None) if input_data.get('publicationVenue') else None,
                'url': input_data['publicationVenue'].get('url', None) if input_data.get('publicationVenue') else None,
                'volume': input_data['journal'].get('volume', None) if input_data.get('journal') else None
            },
            'year': input_data.get('year', None),
            'referenceCount': input_data.get('referenceCount', None),
            'citationCount': input_data.get('citationCount', None),
            'openAccessPdf': input_data['openAccessPdf'].get('url', None) if input_data.get('openAccessPdf') else None,
            'fieldsOfStudy': input_data.get('fieldsOfStudy', None),
            's2FieldsOfStudy': input_data.get('s2FieldsOfStudy', None),
            'authors': input_data.get('authors', None),
            'version': os.getenv('ASSETS_VERSION'),
        }

        input_data_info = get_paper_info(input_data['paperId'], cache)
        if input_data_info:
            scholarlyarticle['embedding'] = json.dumps(input_data_info['embedding'].get('vector', None)) if input_data_info.get('embedding') else None
            scholarlyarticle['citations'] = []
            for j in range(len(input_data_info['citations'])):
                if not all(input_data_info['citations'][j].get(field) is not None for field in ['paperId', 'url', 'title']):
                    continue
                scholarlyarticle['citations'].append({
                    '@id': 'urn:chatdkg:scientific:' + input_data_info['citations'][j].get('paperId', None) + '/' + os.getenv('ASSETS_VERSION'),
                    '@type': 'ScholarlyArticle',
                    'url': input_data_info['citations'][j].get('url', None),
                    'title': input_data_info['citations'][j].get('title', None),
                })
        print(f'Created {i+1} of {len(papers)} knowledge asset')
        result.append(scholarlyarticle)

    return result