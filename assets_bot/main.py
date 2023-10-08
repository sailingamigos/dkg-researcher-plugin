"""Assets bot main module."""

from config.settings import TOPIC, LIMIT, OFFSET, USE_CACHE
from api_crawler import get_papers, Repository
from data_builder.scholarly_article import create_assets as create_scholarly_article_assets
from data_importer.assets_generator import publish_assets

data = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": []
}

for i in range(0, LIMIT, OFFSET):
    papers = get_papers (Repository.SCHOLARLY_ARTICLE, TOPIC, OFFSET, i, USE_CACHE)
    assets = create_scholarly_article_assets (papers['data'])
    data["itemListElement"].append(assets)

publish_assets (data, '../cache/assets.jsonld')
