from datetime import timedelta

from sqlmodel.orm.session import Session
from sqlmodel import select
from sqlalchemy.orm import selectinload

from fastapi.security import OAuth2PasswordRequestForm

from bcrypt import checkpw

from odhbackend.models import Token
from odhbackend.models import User
from odhbackend.models import RoleEnum
from odhbackend.models import UserRole

from odhbackend.exceptions.http_exception import HTTPException

from odhbackend.utils.environment_variables import ACCESS_TOKEN_EXPIRE_MINUTES

from odhbackend.services.structured_data_store_service import engine
from odhbackend.services.jwt_service import create_access_token
from odhbackend.services.jwt_service import get_token_data


class OAuth2Repository:

    @staticmethod
    def get_user_by_email(
            email: str
    ) -> User:
        with Session(engine) as session:
            statement = select(User).options(selectinload(User.user_roles)).where(
                User.email == email
            )
            return session.exec(statement=statement).first()

    @staticmethod
    def login_for_access_token(
            form_data: OAuth2PasswordRequestForm
    ) -> Token:
        """OA01R"""
        where = """OA01R"""
        token: Token

        user = OAuth2Repository.get_user_by_email(email=form_data.username)
        if user is None:
            HTTPException.raise_unauthorized(
                message=f"Usuário não encontrado.",
                where=where
            )
        if not checkpw(password=form_data.password.encode(), hashed_password=user.hashed_password.encode()):
            HTTPException.raise_unauthorized(
                message="Senha incorreta.",
                where=where
            )
        token = Token(access_token=create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        ), token_type="bearer")

        return token

    @staticmethod
    def get_current_user(
            token: str,
            required_roles: list[RoleEnum]
    ) -> User:
        """OA02R"""
        where = """OA02R"""

        token_data = get_token_data(token=token)
        if token_data is None:
            HTTPException.raise_unauthorized(
                detail="Token de acesso inválido.",
                where=where
            )
        user = OAuth2Repository.get_user_by_email(token_data.email)
        if user is None:
            HTTPException.raise_unauthorized(
                where=where
            )
        if required_roles and not OAuth2Repository.user_has_roles(user=user, roles=required_roles):
            HTTPException.raise_unauthorized(
                detail=f"Usuário '{user.email}' não possui atribuição de perfil requerida: {[required_role.value for required_role in required_roles]}.",
                where=where
            )
        return user

    @staticmethod
    def user_has_roles(
            user: User,
            roles: list[RoleEnum]
    ) -> bool:
        """OA03R"""

        with Session(engine) as session:
            results = session.exec(statement=select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role.in_(roles)
            ))
            if len(list(results)) == 0:
                return False
            else:
                return True