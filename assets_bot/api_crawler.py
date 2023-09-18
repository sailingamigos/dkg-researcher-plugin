"""API crawler module."""

from enum import Enum
from data_builder.scholarly_article import fetch_papers as scholarly_fetch
from data_builder.semopenalex import fetch_papers as semopenalex_fetch

class Repository (Enum):
    """Enum for repositories."""
    SCHOLARLY_ARTICLE = 1
    SEMOPENALEX = 2

def get_papers (repository, topic, limit, offset, use_cache):
    """Fetch papers from a repository."""
    if repository == Repository.SCHOLARLY_ARTICLE:
        fetch_func = scholarly_fetch
    else:
        fetch_func = semopenalex_fetch
    print(f"Fetching repository: {repository}, Topic: {topic}, Limit: {limit}, Offset: {offset}")
    return fetch_func (topic, limit, offset, use_cache)
