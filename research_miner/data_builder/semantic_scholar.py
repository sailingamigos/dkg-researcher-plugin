"""Semantic scholar builder module."""

import os
import json
from http.client import HTTPException
from dotenv import load_dotenv
import requests
from helper import get_cache, set_cache, cache_exists # pylint: disable=import-error

load_dotenv()

def get_papers(repository, topic, limit, offset):
    """Fetch papers."""
    cache_path = f'{repository.name}_{topic}/{repository.name}_{topic}_{limit}_{offset}_papers'
    if cache_exists(cache_path):
        return get_cache(cache_path)

    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {
        'query': topic,
        'offset': offset,
        'limit': limit,
        'fields':(
            'paperId,corpusId,url,title,venue,publicationVenue,year,authors,'
            'externalIds,abstract,referenceCount,citationCount,influentialCitationCount,'
            'isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,'
            'publicationDate,journal,citationStyles'
        )
    }
    headers = {'x-api-key': os.getenv('SEMANTIC_SCHOLAR_API_KEY')}

    response = requests.get(url, params=params, headers=headers, timeout=30)

    if response.status_code == 200:
        set_cache(cache_path, json.loads(response.text)['data'])
        return json.loads(response.text)['data']
    else:
        raise HTTPException(f'Failed to fetch data: {response.status_code}')

def create_assets(papers):
    """Create assets."""
    result = []

    for input_data in papers:
        scholarlyarticle = {
            'public': {
                '@context': 'https://schema.org',
                '@id': 'urn:research:' + input_data.get('paperId', None),
                '@type': 'ScholarlyArticle',
                'paperId': input_data.get('paperId', None),
                'corpusId': input_data.get('corpusId', None),
                'url': input_data.get('url', None),
                'title': input_data.get('title', None),
                'venue': input_data.get('venue', None),
                'publicationVenue': {
                    'id': 'urn:research:' + input_data['publicationVenue'].get('id', None) if input_data.get('publicationVenue') else None, # pylint: disable=line-too-long
                    'name': input_data['publicationVenue'].get('name', None) if input_data.get('publicationVenue') else None, # pylint: disable=line-too-long
                    'alternate_names': input_data['publicationVenue'].get('alternate_names', None) if input_data.get('publicationVenue') else None, # pylint: disable=line-too-long
                    'issn': input_data['publicationVenue'].get('issn', None) if input_data.get('publicationVenue') else None, # pylint: disable=line-too-long
                    'url': input_data['publicationVenue'].get('url', None) if input_data.get('publicationVenue') else None # pylint: disable=line-too-long
                },
                'year': input_data.get('year', None),
                'externalIds': input_data.get('externalIds', None),
                'abstract': input_data.get('abstract', None),
                'referenceCount': input_data.get('referenceCount', None),
                'citationCount': input_data.get('citationCount', None),
                'influentialCitationCount': input_data.get('influentialCitationCount', None),
                'isOpenAccess': input_data.get('isOpenAccess', None),
                'openAccessPdf': input_data.get('openAccessPdf', None),
                'fieldsOfStudy': input_data.get('fieldsOfStudy', None),
                's2FieldsOfStudy': input_data.get('s2FieldsOfStudy', None),
                'publicationTypes': input_data.get('publicationTypes', None),
                'publicationDate': input_data.get('publicationDate', None),
                'journal': {
                    'name': input_data['journal'].get('name', None) if input_data.get('journal') else None, # pylint: disable=line-too-long
                    'volume': input_data['journal'].get('volume', None) if input_data.get('journal') else None # pylint: disable=line-too-long
                },
                'citationStyles': input_data.get('citationStyles', None)
            }
        }

        result.append(scholarlyarticle)

    return result
