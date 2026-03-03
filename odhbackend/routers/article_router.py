from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query

from odhbackend.controllers.article_controller import ArticleController
from odhbackend.controllers.oauth2_controller import OAuth2Controller
from odhbackend.models import User

router = APIRouter(prefix="/articles", tags=["Articles Elasticsearch"])
controller = ArticleController()

@router.get("/feed")
async def feed_articles(
    current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)],
    any_keywords: Optional[List[str]] = Query(None, description="OR lógico"),
    all_keywords: Optional[List[str]] = Query(None, description="AND lógico"),
    forbidden_keywords: Optional[List[str]] = Query(None, description="Excluir palavras"),
    source: Optional[str] = Query(None, description="Filtrar por fonte (ex: G1)"),
    start_time: Optional[str] = Query(None, description="Data início ISO 8601"),
    end_time: Optional[str] = Query(None, description="Data fim ISO 8601"),
    page: int = Query(1, description="Número da página", ge=1)
):
    """
    Lista artigos paginados do Elasticsearch utilizando filtros semânticos e temporais.
    """
    return controller.get_feed(
        page=page,
        any_keywords=any_keywords,
        all_keywords=all_keywords,
        forbidden_keywords=forbidden_keywords,
        source=source,
        start_time=start_time,
        end_time=end_time
    )

@router.get("/{article_id}")
async def get_article_by_id(
    current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)],
    article_id: str
):
    """
    Recupera um artigo específico pelo seu ID gerado no Elasticsearch.
    """
    return controller.get_article(article_id)