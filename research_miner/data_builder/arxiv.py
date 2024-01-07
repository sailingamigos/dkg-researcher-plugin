"""Arxiv builder module."""

import os
import feedparser # pylint: disable=import-error
from http.client import HTTPException
from dotenv import load_dotenv # pylint: disable=import-error
import requests
from datetime import datetime
from helper import get_cache, set_cache, cache_exists  # pylint: disable=import-error

load_dotenv()

def get_papers(repository, topic, limit, offset, cache):
    """
    Fetch papers from the Arxiv repository.

    Args:
        repository (str): The name of the repository.
        topic (str): The research topic to search for.
        limit (int): The maximum number of papers to retrieve.
        offset (int): The offset for paginating through results.
        cache (bool): Whether to use caching for results.

    Returns:
        list: List of papers retrieved from Arxiv.
    """
    cache_path = f'{repository.name}_{topic}/{repository.name}_{topic}_{limit}_{offset}_papers'
    if cache and cache_exists(cache_path):
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
        if cache:
            set_cache(cache_path, feed.entries)
        return feed.entries

    raise HTTPException(f'Failed to fetch data: {response.status_code}')

def create_assets(papers, _):
    """
    Create assets from the retrieved papers.

    Args:
        papers (list): List of papers from Arxiv.
        cache (bool): Whether to use caching for assets.

    Returns:
        list: List of assets created from papers.
    """
    result = []

    for input_data in papers:
        arxiv_article = {
            '@context': 'https://schema.org',
            '@type': 'ArxivArticle',
            '@id': 'urn:chatdkg:scientific:' + input_data.get('id', None).split('/')[-1] + '/' + os.getenv('ASSETS_VERSION'),
            'title': input_data.get('title', None),
            'year': datetime.fromisoformat(input_data.get('published', None)).year,
            'abstract': input_data.get('summary', None),
            'authors': [d['name'] for d in input_data.authors],
            'url': [d['href'] for d in input_data.links],
            'primary_category': input_data.arxiv_primary_category['term'],
            "categories": [d['term'] for d in input_data.tags],
            'version': os.getenv('ASSETS_VERSION')
        }

        result.append(arxiv_article)

    return result
