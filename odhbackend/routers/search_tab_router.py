from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy.orm import Session

from odhbackend.tools.dependencies import get_authenticated_user, get_db
from odhbackend.controllers.search_tab_controller import SearchTabController
from odhbackend.schemas.search_tab_models import (
    SearchTabCreate,
    SearchTabEdit,
    KeywordModel,
    DomainModel,
    SearchTabCreateFull,
    SuccessResponse,
    SearchTabListResponse,
    SearchTabDetailResponse
)

# Definimos o router (o prefixo geralmente é configurado no main.py)
router = APIRouter(tags=["Search Tabs"])

# -----------------------------
# Auxiliar para CSRF
# -----------------------------
def validate_csrf_token(request: Request, csrf_protect: CsrfProtect):
    csrf_token = request.headers.get("X-CSRF-Token")
    if not csrf_token:
        raise HTTPException(status_code=403, detail="CSRF token is missing")
    csrf_protect.validate_csrf(csrf_token)

# -----------------------------
# CRUD para SearchTab
# -----------------------------

@router.post("/create", response_model=SuccessResponse)
async def create_search_tab(
    data: SearchTabCreate,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).create_search_tab(user, data)


@router.put("/edit/{tab_id}", response_model=SuccessResponse)
async def edit_search_tab(
    tab_id: int,
    data: SearchTabEdit,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).edit_search_tab(user, tab_id, data)


@router.delete("/delete/{tab_id}", response_model=SuccessResponse)
async def delete_search_tab(
    tab_id: int,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).delete_search_tab(user, tab_id)


@router.get("/get_search_tab/{tab_id}", response_model=SearchTabDetailResponse)
async def get_search_table(
    tab_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_authenticated_user)
):
    return SearchTabController(db).get_search_tab(user, tab_id)


@router.get("/get_user_tab", response_model=SearchTabListResponse)
async def get_search_tabs(
    db: Session = Depends(get_db),
    user: dict = Depends(get_authenticated_user)
):
    return SearchTabController(db).get_user_tabs(user)


@router.post("/create_full", response_model=SuccessResponse)
async def create_full_search_tab(
    request: Request,
    data: SearchTabCreateFull,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).create_full_search_tab(user, data)


# -----------------------------
# CRUD para Keywords e Domains
# -----------------------------

@router.post("/add_any_keyword/{tab_id}", response_model=SuccessResponse)
async def add_any_keyword(
    tab_id: int,
    data: KeywordModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).add_any_keyword(user, tab_id, data)


@router.delete("/remove_any_keyword/{tab_id}", response_model=SuccessResponse)
async def remove_any_keyword(
    tab_id: int,
    data: KeywordModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).remove_any_keyword(user, tab_id, data)


@router.post("/add_all_keyword/{tab_id}", response_model=SuccessResponse)
async def add_all_keyword(
    tab_id: int,
    data: KeywordModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).add_all_keyword(user, tab_id, data)


@router.delete("/remove_all_keyword/{tab_id}", response_model=SuccessResponse)
async def remove_all_keyword(
    tab_id: int,
    data: KeywordModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).remove_all_keyword(user, tab_id, data)


@router.post("/add_forbidden_keyword/{tab_id}", response_model=SuccessResponse)
async def add_forbidden_keyword(
    tab_id: int,
    data: KeywordModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).add_forbidden_keyword(user, tab_id, data)


@router.delete("/remove_forbidden_keyword/{tab_id}", response_model=SuccessResponse)
async def remove_forbidden_keyword(
    tab_id: int,
    data: KeywordModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).remove_forbidden_keyword(user, tab_id, data)


@router.post("/add_forbidden_domain/{tab_id}", response_model=SuccessResponse)
async def add_forbidden_domain(
    tab_id: int,
    data: DomainModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).add_forbidden_domain(user, tab_id, data)


@router.delete("/remove_forbidden_domain/{tab_id}", response_model=SuccessResponse)
async def remove_forbidden_domain(
    tab_id: int,
    data: DomainModel,
    request: Request,
    db: Session = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    user: dict = Depends(get_authenticated_user)
):
    validate_csrf_token(request, csrf_protect)
    return SearchTabController(db).remove_forbidden_domain(user, tab_id, data)