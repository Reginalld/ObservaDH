from sqlmodel.orm.session import Session
from sqlmodel import select
from sqlmodel import delete
from sqlmodel import over
from sqlmodel import func
from bcrypt import gensalt
from bcrypt import hashpw

from odhbackend.models import User
from odhbackend.models import UserPublic
from odhbackend.models import UserCreate
from odhbackend.models import UserUpdate
from odhbackend.models import UserList
from odhbackend.models import UserRole
from odhbackend.models import RoleEnum

from odhbackend.exceptions.http_exception import HTTPException

from odhbackend.utils.functions import random_string
from odhbackend.utils.environment_variables import DEFAULT_USER_PASSWORD

from odhbackend.services.structured_data_store_service import engine


class UserRepository:

    @staticmethod
    def get_user(
            session: Session,
            user_id: str
    ):
        user = session.exec(statement=select(User).where(
            User.id == user_id
        )).first()
        if user is None:
            HTTPException.raise_not_found(
                message="Usuário não encontrado."
            )
        return user

    @staticmethod
    def create_user(
            current_user: User,
            user_create: UserCreate
    ) -> UserPublic:
        """US01R"""
        user_public: UserPublic

        with Session(engine) as session:
            try:
                if session.exec(statement=select(User).where(
                        User.email == user_create.email
                )).first():
                    HTTPException.raise_bad_request(
                        message="E-mail do usuário existe."
                    )

                salt = gensalt()
                hashed_password = hashpw(password=DEFAULT_USER_PASSWORD.encode(), salt=salt).decode()
                user = User(
                    **user_create.model_dump(),
                    id=random_string(),
                    hashed_password=hashed_password
                )
                session.add(user)
                session.flush()

                user.user_roles = [UserRole(
                    user_id=user.id,
                    role=role
                ) for role in user_create.roles]
                session.add(user)
                session.flush()

                user_public = UserPublic(
                    **user.model_dump(),
                    roles=[user_role.role for user_role in user.user_roles]
                )
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        return user_public

    @staticmethod
    def update_user(
            current_user: User,
            user_id: str,
            user_update: UserUpdate
    ) -> UserPublic:
        """US02R"""
        user_public: UserPublic

        with Session(engine) as session:
            try:
                if session.exec(statement=select(User).where(
                        User.id != user_id,
                        User.email == user_update.email
                )).first():
                    HTTPException.raise_bad_request(
                        message="E-mail do usuário existe."
                    )
                user = UserRepository.get_user(
                    session=session,
                    user_id=user_id
                )
                user.email = user_update.email
                user.full_name = user_update.full_name
                user.cpf = user_update.cpf

                session.exec(delete(UserRole).where(
                    UserRole.user_id == user_id
                ))

                user.user_roles = [UserRole(
                    user_id=user_id,
                    role=role
                ) for role in user_update.roles]
                session.flush()

                user_public = UserPublic(
                    **user.model_dump(),
                    roles=[user_role.role for user_role in user.user_roles]
                )
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        return user_public

    @staticmethod
    def read_user(
            current_user: User,
            user_id: str
    ) -> UserPublic:
        """US03R"""
        user_public: UserPublic

        with Session(engine) as session:
            user = UserRepository.get_user(
                session=session,
                user_id=user_id
            )

            user_public = UserPublic(
                **user.model_dump(),
                roles=[user_role.role for user_role in user.user_roles]
            )

        return user_public

    @staticmethod
    def read_users(
            current_user: User,
            offset: int,
            limit: int,
            term: str | None,
            roles: list[RoleEnum] | None,
            full_name_desc: bool | None
    ) -> UserList:
        """US05R"""
        user_list: UserList

        with Session(engine) as session:
            statement = select(User, over(func.count()).label("count"))
            if term:
                statement = statement.where(
                    User.full_name.ilike(f"%{term}%")
                )
            if roles:
                statement = statement.where(
                    User.user_roles.any(UserRole.role.in_(roles))
                )
            if full_name_desc:
                statement = statement.order_by(User.full_name.desc())
            else:
                statement = statement.order_by(User.full_name)
            results = session.exec(statement=statement.offset((offset - 1) * limit).limit(limit)).all()

            users = []
            for result in results:
                user = result.User
                users.append(UserPublic(
                    **user.model_dump(),
                    roles=[user_role.role for user_role in user.user_roles]
                ))
            count = results[0].count if results else 0
            user_list = UserList(
                users=users,
                count=count
            )

        return user_list