from typing import List, Optional
from odhbackend.models import User
from odhbackend.exceptions.http_exception import HTTPException
from odhbackend.services.article_service import ArticleService

class ArticleController:
    def __init__(self, service: ArticleService):
        self.service = service

    def get_feed(
        self,
        current_user: User,
        page: int,
        any_keywords: Optional[List[str]],
        all_keywords: Optional[List[str]],
        forbidden_keywords: Optional[List[str]],
        source: Optional[str],
        start_time: Optional[str],
        end_time: Optional[str]
    ) -> dict:
        """
        AR01C - Orquestra a chamada de listagem e avalia o resultado.
        """
        where = "AR01C"
        try:
            result = self.service.get_paginated_feed(
                current_user=current_user,
                page=page,
                any_keywords=any_keywords,
                all_keywords=all_keywords,
                forbidden_keywords=forbidden_keywords,
                source=source,
                start_time=start_time,
                end_time=end_time
            )

            if not result.get("articles"):
                HTTPException.raise_not_found(
                    message="Nenhum artigo encontrado com os filtros fornecidos.",
                    where=where
                )
                
            return result

        except HTTPException:
            raise
        except Exception as e:
            HTTPException.raise_internal_server_error(e=e, where=where)
            return None

    def get_article(
        self, 
        current_user: User,
        article_id: str
    ) -> dict:
        """
        AR02C - Orquestra a chamada de um único artigo e avalia erros.
        """
        where = "AR02C"
        try:
            result = self.service.get_article_detail(
                current_user=current_user,
                article_id=article_id
            )
            
            if result.get("status") == "error":
                HTTPException.raise_not_found(
                    message=result.get("message"),
                    where=where
                )
                
            return result.get("data")
            
        except Exception as e:
            HTTPException.raise_internal_server_error(e=e, where=where)
            return None

    def search(
        self,
        current_user: User,
        any_keywords: Optional[List[str]],
        all_keywords: Optional[List[str]],
        forbidden_keywords: Optional[List[str]],
        source: Optional[str],
        start_time: Optional[str],
        end_time: Optional[str]
    ) -> dict | None:
        """AR03C"""
        where = "AR03C"
        try:
            result = self.service.search_full(
                current_user=current_user,
                any_keywords=any_keywords,
                all_keywords=all_keywords,
                forbidden_keywords=forbidden_keywords,
                source=source,
                start_time=start_time,
                end_time=end_time
            )

            if not result.get("articles"):
                HTTPException.raise_not_found(
                    message="Nenhum artigo encontrado com os filtros fornecidos.",
                    where=where
                )
                
            return result
        except Exception as e:
            HTTPException.raise_internal_server_error(e=e, where=where)
            return None

    def get_sources_count(
        self,
        current_user: User,
        any_keywords: Optional[List[str]],
        all_keywords: Optional[List[str]],
        forbidden_keywords: Optional[List[str]],
        start_time: Optional[str],
        end_time: Optional[str]
    ) -> dict | None:
        """AR04C"""
        where = "AR04C"
        try:
            return self.service.get_sources_aggregation(
                current_user=current_user,
                any_keywords=any_keywords,
                all_keywords=all_keywords,
                forbidden_keywords=forbidden_keywords,
                start_time=start_time,
                end_time=end_time
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(e=e, where=where)
            return None