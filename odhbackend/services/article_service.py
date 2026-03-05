from typing import List, Optional
from odhbackend.models import User, Article
from odhbackend.domain.interfaces.article_repository import IArticleRepository

class ArticleService:
    """
    Serviço de Artigos que coordena a lógica de negócio.
    Ele depende da interface IArticleRepository e não do Elastic diretamente.
    """

    def __init__(self, repository: IArticleRepository) -> None:
        self.repository = repository

    def get_paginated_feed(
        self,
        current_user: User,
        page: int = 1,
        size: int = 25,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """
        AR01: Processa o feed paginado.
        """
        size = 25
        skip = (page - 1) * size if page >= 1 else 0

        raw_result = self.repository.search(
            current_user=current_user,
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            source=source,
            start_time=start_time,
            end_time=end_time,
            skip=skip,
            limit=size
        )

        hits_data = raw_result.get("hits", {})
        total_results = hits_data.get("total", {}).get("value", 0)
        hits = hits_data.get("hits", [])

        articles = [
            Article(id=hit["_id"], **hit["_source"]) 
            for hit in hits
        ]

        total_pages = (total_results + size - 1) // size

        return {
            "articles": articles,
            "total": total_results,
            "page": page,
            "size": size,
            "total_pages": total_pages,
        }

    def get_article_detail(
        self, 
        current_user: User,
        article_id: str
    ) -> dict:
        """
        AR02: Recupera os detalhes de um artigo único.
        """
        article_source = self.repository.get_by_id(
            current_user=current_user,
            article_id=article_id
        )
        
        if not article_source:
            return {"status": "error", "message": "Artigo não encontrado."}
        
        
        return {"status": "success", "data": Article(id=article_id, **article_source)}
    
    def search_full(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """
        AR03: Busca geral de artigos (sem paginação estrita, limite de 100).
        """
        raw_result = self.repository.search(
            current_user=current_user,
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            source=source,
            start_time=start_time,
            end_time=end_time,
            skip=0,
            limit=100
        )

        hits = raw_result.get("hits", {}).get("hits", [])
        articles = [ArticleDTO(id=hit["_id"], **hit["_source"]) for hit in hits]

        return {"articles": articles}

    def get_sources_aggregation(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """
        AR04: Processa a agregação de fontes do Elasticsearch.
        """
        raw_result = self.repository.count_by_source(
            current_user=current_user,
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            start_time=start_time,
            end_time=end_time
        )
        
        buckets = raw_result.get("aggregations", {}).get("sources", {}).get("buckets", [])
        
        formatted_sources = {b["key"]: b["doc_count"] for b in buckets}

        return {"sources": formatted_sources}