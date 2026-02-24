from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel.orm.session import Session

from typing import Annotated

from fastapi import Depends

from odhbackend.utils.environment_variables import POSTGRES_USER
from odhbackend.utils.environment_variables import POSTGRES_PASSWORD
from odhbackend.utils.environment_variables import POSTGRES_HOST
from odhbackend.utils.environment_variables import POSTGRES_PORT
from odhbackend.utils.environment_variables import POSTGRES_DB

connect_args = {"connect_timeout": 5}
engine = create_engine(
    url=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class StructuredDataStoreService:
    pass
