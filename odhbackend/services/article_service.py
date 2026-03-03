from typing import List, Optional
from odhbackend.repositories.article_repository import ArticleRepository

class ArticleService:
    def __init__(self):
        self.repository = ArticleRepository()

    def get_paginated_feed(
        self,
        page: int = 1,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """
        Processa os parâmetros de paginação e formata a resposta do repositório.
        """
        size = 25
        from_ = (page - 1) * size if page >= 1 else 0

        raw_result = self.repository.search_articles(
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            source=source,
            start_time=start_time,
            end_time=end_time,
            from_=from_,
            size=size
        )

        hits_data = raw_result.get("hits", {})
        total_results = hits_data.get("total", {}).get("value", 0)
        hits = hits_data.get("hits", [])

        articles = []
        for hit in hits:
            article = hit["_source"]
            article["id"] = hit["_id"]  # Injeta o ID para o front-end
            articles.append(article)

        total_pages = (total_results + size - 1) // size

        return {
            "articles": articles,
            "total": total_results,
            "page": page,
            "size": size,
            "total_pages": total_pages,
        }

    def get_single_article(self, article_id: str) -> dict:
        """
        Busca uma notícia única e padroniza a resposta.
        """
        article = self.repository.get_article_by_id(article_id)
        if not article:
            return {"status": "error", "message": "Artigo não encontrado."}
        
        article["id"] = article_id
        return {"status": "success", "data": article}