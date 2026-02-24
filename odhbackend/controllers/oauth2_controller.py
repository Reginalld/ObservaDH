from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from odhbackend.models import Token, User, RoleEnum
from odhbackend.repositories.oauth2_repository import OAuth2Repository
from odhbackend.exceptions.http_exception import HTTPException


class OAuth2Controller:

    def __init__(
            self,
            required_roles: list[RoleEnum]
    ) -> None:
        self.repository = OAuth2Repository()
        self.required_roles = required_roles

    def login_for_access_token(
            self,
            form_data: OAuth2PasswordRequestForm
    ) -> Token:
        """OA01C"""
        where = "OA01C"
        try:
            return self.repository.login_for_access_token(
                form_data=form_data
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )
            return None

    def get_current_user(
            self,
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ) -> User | None:
        """OA02C"""
        where = "OA02C"
        try:
            return self.repository.get_current_user(
                token=token,
                required_roles=self.required_roles
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )

    def user_has_roles(
            self,
            user: User,
            roles: list[RoleEnum]
    ) -> bool:
        """OA03C"""
        where = "OA03C"
        try:
            return self.repository.user_has_roles(
                user=user,
                roles=roles
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )
            return None