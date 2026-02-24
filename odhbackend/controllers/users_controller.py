from re import match

from odhbackend.constants import USER_EMAIL_MAX_LENGTH
from odhbackend.constants import USER_FULL_NAME_MAX_LENGTH
from odhbackend.constants import USER_FULL_NAME_MIN_LENGTH
from odhbackend.constants import USER_CPF_MAX_LENGTH
from odhbackend.constants import USER_CPF_MIN_LENGTH
from odhbackend.models import User
from odhbackend.models import UserPublic
from odhbackend.models import UserCreate
from odhbackend.models import UserUpdate
from odhbackend.models import UserList
from odhbackend.models import RoleEnum
from odhbackend.repositories.users_repository import UserRepository
from odhbackend.exceptions.http_exception import HTTPException
from odhbackend.utils.functions import is_valid_id


class UserController:

    def __init__(self) -> None:
        self.repository = UserRepository()

    def create_user(
            self,
            current_user: User,
            user_create: UserCreate
    ) -> UserPublic:
        """US01C"""
        where = "US01C"
        try:
            if len(user_create.email) > USER_EMAIL_MAX_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"E-mail muito longo.",
                    where=where
                )
            if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user_create.email):
                HTTPException.raise_bad_request(
                    message=f"E-mail não é válido.",
                    where=where
                )
            if len(user_create.full_name) > USER_FULL_NAME_MAX_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"Nome muito longo.",
                    where=where
                )
            if len(user_create.full_name) < USER_FULL_NAME_MIN_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"Nome muito curto.",
                    where=where
                )
            if len(user_create.cpf) > USER_CPF_MAX_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"CPF muito longo.",
                    where=where
                )
            if len(user_create.cpf) < USER_CPF_MIN_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"CPF muito curto.",
                    where=where
                )
            if not user_create.cpf.isdigit():
                HTTPException.raise_bad_request(
                    message="CPF deve conter apenas números.",
                    where=where
                )
            return self.repository.create_user(
                current_user=current_user,
                user_create=user_create
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )
            return None

    def update_user(
            self,
            current_user: User,
            user_id: str,
            user_update: UserUpdate
    ) -> UserPublic:
        """US02C"""
        where = "US02C"
        try:
            if not is_valid_id(id_to_validate=user_id):
                HTTPException.raise_bad_request(message="ID inválido.")
            if len(user_update.email) > USER_EMAIL_MAX_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"E-mail muito longo.",
                    where=where
                )
            if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user_update.email):
                HTTPException.raise_bad_request(
                    message=f"E-mail não é válido.",
                    where=where
                )
            if len(user_update.full_name) > USER_FULL_NAME_MAX_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"Nome muito longo.",
                    where=where
                )
            if len(user_update.full_name) < USER_FULL_NAME_MIN_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"Nome muito curto.",
                    where=where
                )
            if len(user_update.cpf) > USER_CPF_MAX_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"CPF muito longo.",
                    where=where
                )
            if len(user_update.cpf) < USER_CPF_MIN_LENGTH:
                HTTPException.raise_bad_request(
                    message=f"CPF muito curto.",
                    where=where
                )
            if not user_update.cpf.isdigit():
                HTTPException.raise_bad_request(
                    message="CPF deve conter apenas números.",
                    where=where
                )
            return self.repository.update_user(
                current_user=current_user,
                user_id=user_id,
                user_update=user_update
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )
            return None

    def read_user(
            self,
            current_user: User,
            user_id: str
    ) -> UserPublic:
        """US03C"""
        where = "US03C"
        try:
            if not is_valid_id(id_to_validate=user_id):
                HTTPException.raise_bad_request(message="ID inválido.")
            return self.repository.read_user(
                current_user=current_user,
                user_id=user_id
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )
            return None

    def read_users(
            self,
            current_user: User,
            offset: int,
            limit: int,
            term: str | None,
            roles: list[RoleEnum] | None,
            full_name_desc: bool | None
    ) -> UserList | None:
        """US04C"""
        where = "US04C"
        try:
            return self.repository.read_users(
                current_user=current_user,
                offset=offset,
                limit=limit,
                term=term,
                roles=roles,
                full_name_desc=full_name_desc
            )
        except Exception as e:
            HTTPException.raise_internal_server_error(
                e=e,
                where=where
            )