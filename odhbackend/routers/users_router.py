from typing import Annotated
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from odhbackend.models import User
from odhbackend.models import RoleEnum
from odhbackend.models import UserPublic
from odhbackend.models import UserCreate
from odhbackend.models import UserUpdate
from odhbackend.models import UserList

from odhbackend.controllers.oauth2_controller import OAuth2Controller
from odhbackend.controllers.users_controller import UserController

users_router = APIRouter(tags=["users"])


@users_router.post(
    path="/users",
    response_model=UserPublic,
    name="create_user",
    summary="US01: criar usuário",
    description="Cria usuário. "
                "É preciso possuir atribuição de perfil 'Coordenação'. "
                "Atualiza dados na base relacional PostGIS."
)
async def create_user(
        current_user: Annotated[User, Depends(OAuth2Controller(
            required_roles=[RoleEnum.coordination]
        ).get_current_user)],
        user_create: UserCreate
) -> UserPublic:
    return UserController().create_user(
        current_user=current_user,
        user_create=user_create
    )

@users_router.get(
    path="/users",
    response_model=UserList,
    name="read_users",
    summary="US02: recuperar usuários",
    description="Recupera usuários. "
                "É preciso possuir atribuição de perfil 'Coordenação'. "
                "Recupera dados da base relacional PostGIS."
)
async def read_users(
        current_user: Annotated[User, Depends(OAuth2Controller(
            required_roles=[RoleEnum.coordination]
        ).get_current_user)],
        offset: Optional[int] = Query(default=1, ge=1),
        limit: Optional[int] = Query(default=10, ge=1, le=100),
        term: Optional[str] = Query(default=None),
        roles: Optional[list[RoleEnum]] = Query(default=None),
        full_name_desc: Optional[bool] = Query(default=False)
) -> UserList:
    return UserController().read_users(
        current_user=current_user,
        offset=offset,
        limit=limit,
        term=term,
        roles=roles,
        full_name_desc=full_name_desc
    )


@users_router.get(
    path="/me",
    response_model=UserPublic,
    name="read_current_user",
    summary="US03: recuperar usuário atual",
    description="Recupera usuário atual. "
                "Recupera dados da base relacional PostGIS."
)
async def read_current_user(
        current_user: Annotated[User, Depends(OAuth2Controller(required_roles=[]).get_current_user)]
) -> UserPublic:
    user_roles = getattr(current_user, "user_roles", []) or []
    roles = [user_role.role for user_role in user_roles]
    return UserPublic(**current_user.model_dump(), roles=roles)

@users_router.put(
    path="/users/{user_id}",
    response_model=UserPublic,
    name="update_user",
    summary="US04: atualizar usuário",
    description="Atualiza usuário. "
                "É preciso possuir atribuição de perfil 'Coordenação'. "
                "Atualiza dados na base relacional PostGIS."
)
async def update_user(
        current_user: Annotated[User, Depends(OAuth2Controller(
            required_roles=[RoleEnum.coordination]
        ).get_current_user)],
        user_id: str,
        user_update: UserUpdate
) -> UserPublic:
    return UserController().update_user(
        current_user=current_user,
        user_id=user_id,
        user_update=user_update
    )


@users_router.get(
    path="/users/{user_id}",
    response_model=UserPublic,
    name="read_user",
    summary="US05: recuperar usuário",
    description="Recupera usuário. "
                "É preciso possuir atribuição de perfil 'Coordenação'. "
                "Recupera dados da base relacional PostGIS."
)
async def read_user(
        current_user: Annotated[User, Depends(OAuth2Controller(
            required_roles=[RoleEnum.coordination]
        ).get_current_user)],
        user_id: str
) -> UserPublic:
    return UserController().read_user(
        current_user=current_user,
        user_id=user_id
    )