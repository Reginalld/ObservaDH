import os
from elasticsearch import Elasticsearch
from odhbackend.repositories.es_article_repository import ESArticleRepository
from odhbackend.services.article_service import ArticleService

_host = 'elasticsearch_container' if os.path.exists('/.dockerenv') else 'localhost'
es_client = Elasticsearch([f"http://{_host}:9200"])

def get_article_service() -> ArticleService:
    repo = ESArticleRepository(client=es_client)
    return ArticleService(repository=repo)