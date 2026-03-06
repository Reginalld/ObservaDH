import os
from elasticsearch import Elasticsearch
from fastapi import Depends
from sqlmodel import Session

from odhbackend.services.structured_data_store_service import get_session

from odhbackend.repositories.es_article_repository import ESArticleRepository
from odhbackend.services.article_service import ArticleService

_host = 'elasticsearch_container' if os.path.exists('/.dockerenv') else 'localhost'
es_client = Elasticsearch([f"http://{_host}:9200"])

def get_article_service(db: Session = Depends(get_session)) -> ArticleService:
    repo = ESArticleRepository(client=es_client)
    
    return ArticleService(repository=repo, db=db)