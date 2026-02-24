from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from odhbackend.utils.environment_variables import ACCESS_TOKEN_EXPIRE_MINUTES
from odhbackend.models import Token
from odhbackend.controllers.oauth2_controller import OAuth2Controller

oauth2_router = APIRouter(tags=["oauth2"])


@oauth2_router.post(
    path="/token",
    response_model=Token,
    name="login_for_access_token",
    summary="OA01: login para token de acesso",
    description="Login para token de acesso. "
                f"Recupera um token de acesso válido por {ACCESS_TOKEN_EXPIRE_MINUTES} minutos por intermédio do e-mail e da senha do usuário."
)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return OAuth2Controller(required_roles=[]).login_for_access_token(form_data=form_data)