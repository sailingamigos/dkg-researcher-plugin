"""Scholarly article builder module."""

import os
import json
from http.client import HTTPException
from dotenv import load_dotenv
import requests
from data_importer.cache_helper import get_cache, set_cache, cache_exists # pylint: disable=import-error

load_dotenv()

def fetch_papers (topic, limit, offset, use_cache):
    """Fetch papers."""
    if use_cache and cache_exists (f'{topic}_{limit}_{offset}_papers'):
        return get_cache (f'{topic}_{limit}_{offset}_papers')

    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": topic,
        "offset": offset,
        "limit": limit,
        "fields": (
            "paperId,corpusId,url,title,venue,publicationVenue,year,authors,"
            "externalIds,abstract,referenceCount,citationCount,influentialCitationCount,"
            "isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,"
            "publicationDate,journal,citationStyles,embedding,tldr"
        )
    }
    headers = {"x-api-key": os.getenv("SEMANTIC_SCHOLAR_API_KEY")}

    response = requests.get(url, params=params, headers=headers, timeout=30)

    if response.status_code == 200:
        if use_cache:
            set_cache (f'{topic}_{limit}_{offset}_papers', response.text)
        return json.loads(response.text)
    else:
        raise HTTPException(f"Failed to fetch data: {response.status_code}")

def create_assets (papers):
    """Create assets."""
    result = []

    for input_data in papers:
        scholarlyarticle = {
            '@id': input_data.get('paperId', None),
            '@type': "ScholarlyArticle",
            'paperId': input_data.get('paperId', None),
            'corpusId': input_data.get('corpusId', None),
            'url': input_data.get('url', None),
            'title': input_data.get('title', None),
            'venue': input_data.get('venue', None),
            'publicationVenue': {
                'id': input_data['publicationVenue'].get('id', None) if input_data.get('publicationVenue') else None, # pylint: disable=line-too-long
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

        result.append(scholarlyarticle)

    return result
