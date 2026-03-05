from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query

from odhbackend.models import User
from odhbackend.models import Article
from odhbackend.models import PaginatedArticleResponse
from odhbackend.controllers.oauth2_controller import OAuth2Controller
from odhbackend.controllers.article_controller import ArticleController
from odhbackend.utils.dependencies import get_article_service
from odhbackend.services.article_service import ArticleService

articles_router = APIRouter(tags=["Articles Elasticsearch"])


@articles_router.get(
    path="/feed",
    name="feed_articles",
    summary="AR01: listar feed de artigos",
    description="Lista artigos paginados do Elasticsearch utilizando filtros semânticos e temporais."
)
async def feed_articles(
    current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)],
    service: Annotated[ArticleService, Depends(get_article_service)],
    page: Optional[int] = Query(default=1, ge=1),
    any_keywords: Optional[List[str]] = Query(default=None, description="OR lógico"),
    all_keywords: Optional[List[str]] = Query(default=None, description="AND lógico"),
    forbidden_keywords: Optional[List[str]] = Query(default=None, description="Excluir palavras"),
    source: Optional[str] = Query(default=None, description="Filtrar por fonte (ex: G1)"),
    start_time: Optional[str] = Query(default=None, description="Data início ISO 8601"),
    end_time: Optional[str] = Query(default=None, description="Data fim ISO 8601")
) -> dict:
    return service.get_paginated_feed(
        current_user=current_user,
        page=page,
        size=25,
        any_keywords=any_keywords,
        all_keywords=all_keywords,
        forbidden_keywords=forbidden_keywords,
        source=source,
        start_time=start_time,
        end_time=end_time
    )

@articles_router.get(
    path="/search",
    name="search_articles",
    summary="AR03: busca de artigos não paginada",
    description="Busca artigos no Elasticsearch sem os limites estritos da paginação."
)
async def search_articles_by_keywords(
    current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)],
    service: Annotated[ArticleService, Depends(get_article_service)], # Injeção
    any_keywords: Optional[List[str]] = Query(default=None, description="OR lógico"),
    all_keywords: Optional[List[str]] = Query(default=None, description="AND lógico"),
    forbidden_keywords: Optional[List[str]] = Query(default=None, description="Excluir palavras"),
    source: Optional[str] = Query(default=None, description="Filtrar por fonte (ex: G1)"),
    start_time: Optional[str] = Query(default=None, description="Data início ISO 8601"),
    end_time: Optional[str] = Query(default=None, description="Data fim ISO 8601")
) -> dict:
    return service.search_full(
        current_user=current_user,
        any_keywords=any_keywords,
        all_keywords=all_keywords,
        forbidden_keywords=forbidden_keywords,
        source=source,
        start_time=start_time,
        end_time=end_time
    )

@articles_router.get(
    path="/search/sources",
    name="search_sources",
    summary="AR04: contagem de fontes",
    description="Lista todas as fontes disponíveis e suas contagens com base nas keywords."
)
async def search_sources_by_keywords(
    current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)],
    service: Annotated[ArticleService, Depends(get_article_service)], # Injeção
    any_keywords: Optional[List[str]] = Query(default=None, description="OR lógico"),
    all_keywords: Optional[List[str]] = Query(default=None, description="AND lógico"),
    forbidden_keywords: Optional[List[str]] = Query(default=None, description="Excluir palavras"),
    start_time: Optional[str] = Query(default=None, description="Data início ISO 8601"),
    end_time: Optional[str] = Query(default=None, description="Data fim ISO 8601")
) -> dict:
    return service.get_sources_aggregation(
        current_user=current_user,
        any_keywords=any_keywords,
        all_keywords=all_keywords,
        forbidden_keywords=forbidden_keywords,
        start_time=start_time,
        end_time=end_time
    )

@articles_router.get(
    path="/{article_id}",
    name="get_article_by_id",
    summary="AR02: recuperar artigo",
    description="Recupera um artigo específico pelo seu ID gerado no Elasticsearch."
)
async def get_article_by_id(
    current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)],
    service: Annotated[ArticleService, Depends(get_article_service)], # Injeção
    article_id: str
) -> dict:
    return service.get_article_detail(
            current_user=current_user,
            article_id=article_id
        )