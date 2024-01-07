"""Main module."""

import os
from enum import Enum
from dotenv import load_dotenv # pylint: disable=import-error
from data_builder.semantic_scholar import create_assets as create_semantic_scholar, get_papers as get_semantic_scholar
from data_builder.arxiv import create_assets as create_arxiv, get_papers as get_arxiv
from data_publisher.dkg_client import publish_assets

load_dotenv()

class Repository(Enum):
    """Enumeration for data repositories."""
    SEMANTIC_SCHOLAR = 1
    ARXIV = 2

def get_papers(repository, topic, batch, offset, limit, cache):
    """Fetch papers from a specific repository."""
    repository_mapping = {
        Repository.SEMANTIC_SCHOLAR: get_semantic_scholar,
        Repository.ARXIV: get_arxiv
    }
    
    if repository not in repository_mapping:
        raise RuntimeError('Unknown data repository')

    fetch_callback = repository_mapping[repository]
    progress = (offset + batch) * 100 / limit
    print(f'Fetching {topic} papers from {repository} ({progress:.2f}% completed - {offset + batch}/{limit})')
    return fetch_callback(repository, topic, batch, offset, cache)

def create_assets(repository, papers, cache):
    """Generate knowledge assets from retrieved papers."""
    repository_mapping = {
        Repository.SEMANTIC_SCHOLAR: create_semantic_scholar,
        Repository.ARXIV: create_arxiv
    }
    
    if repository not in repository_mapping:
        raise RuntimeError('Unknown data repository')

    create_callback = repository_mapping[repository]
    return create_callback(papers, cache)

def main():
    """Main execution function."""
    repository = Repository(int(os.getenv('REPOSITORY')))
    topics = os.getenv('TOPICS').split(',')
    limit = int(os.getenv('TOPIC_LIMIT'))
    batch = int(os.getenv('TOPIC_BATCH'))
    cache = os.getenv('CACHE') == 'True'

    for topic in topics:
        assets = []
        for i in range(0, limit, batch):
            papers = get_papers(repository, topic, batch, i, limit, cache)
            assets += create_assets(repository, papers, cache)
            print(f'Created {len(assets)} knowledge assets.')
        if assets:
            publish_assets(f'{repository.name}_{topic}/{repository.name}_{topic}', assets)

if __name__ == "__main__":
    main()
