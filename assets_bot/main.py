"""Assets bot main module."""

from config.settings import TOPIC, LIMIT, OFFSET, USE_CACHE
from api_crawler import get_papers, Repository
from data_builder.scholarly_article import create_assets as create_scholarly_article_assets

for i in range(0, LIMIT, OFFSET):
    papers = get_papers (Repository.SCHOLARLY_ARTICLE, TOPIC, OFFSET, i, USE_CACHE)
    assets = create_scholarly_article_assets (papers['data'])
    # dkg.publish ()
