from fastapi import HTTPException
from typing import List, Optional
from odhbackend.services.article_service import ArticleService

class ArticleController:
    def __init__(self):
        self.service = ArticleService()

    def get_feed(
        self,
        page: int,
        any_keywords: Optional[List[str]],
        all_keywords: Optional[List[str]],
        forbidden_keywords: Optional[List[str]],
        source: Optional[str],
        start_time: Optional[str],
        end_time: Optional[str]
    ) -> dict:
        """
        Orquestra a chamada de listagem e avalia o resultado.
        """
        result = self.service.get_paginated_feed(
            page=page,
            any_keywords=any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            source=source,
            start_time=start_time,
            end_time=end_time
        )

        if not result.get("articles"):
            raise HTTPException(
                status_code=404, 
                detail="Nenhum artigo encontrado com os filtros fornecidos."
            )
            
        return result

    def get_article(self, article_id: str) -> dict:
        """
        Orquestra a chamada de um único artigo e avalia erros.
        """
        result = self.service.get_single_article(article_id)
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=404, 
                detail=result.get("message")
            )
            
        return result.get("data")