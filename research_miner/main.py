"""Assets bot main module."""

import os
from enum import Enum
from dotenv import load_dotenv
from data_builder.semantic_scholar import create_assets as create_semantic_scholar, get_papers as get_semantic_scholar
from data_builder.arxiv import create_assets as create_arxiv, get_papers as get_arxiv
from data_importer.dkg_client import publish_assets

load_dotenv()

class Repository(Enum):
    """Enum for data repositories."""
    SEMANTIC_SCHOLAR = 1
    ARXIV = 2

def get_papers(repository, topic, batch, offset):
    """Fetch papers from a repository."""
    if repository == Repository.SEMANTIC_SCHOLAR:
        cb = get_semantic_scholar
    elif repository == Repository.ARXIV:
        cb = get_arxiv
    else:
        raise RuntimeError('Unknown data repository')
    print(f'Fetching repository: {repository}, Topic: {topic}, Batch: {batch}, Offset: {offset}')
    return cb(repository, topic, batch, offset)

def create_assets(repository, papers):
    """Create knowledge assets."""
    if repository == Repository.SEMANTIC_SCHOLAR:
        cb = create_semantic_scholar
    elif repository == Repository.ARXIV:
        cb = create_arxiv
    else:
        raise RuntimeError('Unknown data repository')
    return cb(papers)

def main():
    """Main function."""
    repository = Repository(int(os.getenv('REPOSITORY')))
    topics = os.getenv('TOPICS').split(',')
    limit = int(os.getenv('TOPIC_LIMIT'))
    batch = int(os.getenv('TOPIC_BATCH'))

    for topic in topics:
        for i in range(0, limit, batch):
            papers = get_papers(repository, topic, batch, i)
            assets = create_assets(repository, papers)
            print(f'Publish: {repository}, Topic: {topic}, Assets: {len(assets)}')
            if assets:
                publish_assets(f'{repository.name}_{topic}/{repository.name}_{topic}_{i}', assets)

if __name__ == "__main__":
    main()
