"""Arxiv builder module."""

import feedparser
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

    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'all:{topic}',
        'start': offset,
        'max_results': limit,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 200:
        feed = feedparser.parse(response.text)
        set_cache(cache_path, feed.entries)
        return feed.entries
    else:
        raise HTTPException(f'Failed to fetch data: {response.status_code}')

def create_assets(papers):
    """Create assets."""
    result = []

    for input_data in papers:
        atom = {
            'public': {
                '@context': 'http://www.w3.org/2005/Atom',
                '@type': 'Entry',
                '@id': 'urn:research:' + input_data.get('id', None),
                'title': input_data.get('title', None),
                'updated': input_data.get('updated', None),
                'published': input_data.get('published', None),
                'summary': input_data.get('summary', None),
                'author': [d['name'] for d in input_data.authors],
                'link': [d['href'] for d in input_data.links],
                'primary_category': input_data.arxiv_primary_category['term'],
                "category": [d['term'] for d in input_data.tags]
            }
        }

        result.append(atom)

    return result
