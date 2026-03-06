import os
from typing import List, Optional
from elasticsearch import Elasticsearch
from odhbackend.domain.interfaces.article_repository import IArticleRepository
from odhbackend.models import User

class ESArticleRepository(IArticleRepository):
    def __init__(self, client: Elasticsearch):
        self.client = client
        self.index_name = "articles"

    def _build_query(
        self,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """Monta o JSON da query DSL do Elasticsearch"""
        query = {"bool": {}}

        if any_keywords:
            query["bool"]["should"] = [
                {"match": {"content": {"query": k.lower(), "operator": "or"}}}
                for k in any_keywords
            ]
            query["bool"]["minimum_should_match"] = 1

        if all_keywords:
            query["bool"]["must"] = [
                {"match": {"content": {"query": k.lower(), "operator": "and"}}}
                for k in all_keywords
            ]

        if forbidden_keywords:
            query["bool"]["must_not"] = [
                {"terms": {"content": [k.lower() for k in forbidden_keywords]}}
            ]

        filters = []
        if source:
            filters.append({"term": {"source": source}})
        
        if start_time or end_time:
            date_filter = {"range": {"timestamp": {}}}
            if start_time:
                date_filter["range"]["timestamp"]["gte"] = start_time
            if end_time:
                date_filter["range"]["timestamp"]["lte"] = end_time
            filters.append(date_filter)

        if filters:
            query["bool"]["filter"] = filters

        return query

    def search(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        skip: int = 0,
        limit: int = 25
    ) -> dict:
        """AR01R - Implementação da busca paginada"""
        
        query = self._build_query(
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            source=source,
            start_time=start_time,
            end_time=end_time
        )

        try:
            return self.client.search(
                index=self.index_name,
                query=query,
                from_=skip,
                size=limit,
                sort=[{"timestamp": {"order": "desc"}}]
            )
        except Exception as e:
            print(f"[Elasticsearch Error] Falha na busca AR01R: {e}")
            raise e

    def get_by_id(
        self,
        current_user: User,
        article_id: str
    ) -> Optional[dict]:
        """AR02R - Implementação da busca por ID único"""
        
        try:
            response = self.client.get(index=self.index_name, id=article_id)
            return response.get("_source")
        except Exception as e:
            print(f"[Elasticsearch Error] Falha ao buscar ID {article_id} AR02R: {e}")
            return None

    def count_by_source(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """AR03R - Implementação da agregação de fontes"""
        
        query = self._build_query(
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            start_time=start_time,
            end_time=end_time
        )

        body = {
            "query": query,
            "size": 0,
            "aggs": {
                "sources": {
                    "terms": {
                        "field": "source.keyword",
                        "size": 50 
                    }
                }
            }
        }

        try:
            return self.client.search(index=self.index_name, body=body)
        except Exception as e:
            print(f"[Elasticsearch Error] Falha na agregação AR03R: {e}")
            raise e
        
    def index(self, doc_id: str, document: dict):
        return self.client.index(index=self.index_name, id=doc_id, document=document)