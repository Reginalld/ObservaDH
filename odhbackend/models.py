from typing import Optional
import enum
from sqlmodel import SQLModel, Field, Relationship, Enum, Column


class DefaultResponse(SQLModel):
    detail: str = Field()

class Base(SQLModel):
    id: str = Field(
        primary_key=True,
        max_length=22
    )

class ListBase(SQLModel):
    count: int = Field()


class URLAccess(SQLModel):
    accessed_on: str = Field()
    accessed_url: Optional[str] = Field(default="")
    user_email: Optional[str] = Field(default="")
    previous_url: Optional[str] = Field(default="")
    previous_url_accessed_on: str = Field()

class URLShare(SQLModel):
    shared_on: str = Field()
    shared_url: str = Field()
    user_email: Optional[str] = Field(default="")



class Token(SQLModel):
    access_token: str = Field()
    token_type: str = Field()

class TokenData(SQLModel):
    email: Optional[str] = Field(default=None)


class RoleEnum(enum.Enum):
    dpo = "dpo"
    coordination = "coordination"
    indicators = "indicators"
    communication = "communication"

class UserRole(SQLModel, table=True):
    user_id: str = Field(
        foreign_key="user.id",
        primary_key=True
    )
    role: "RoleEnum" = Field(
        sa_column=Column(
            Enum(RoleEnum),
            primary_key=True
        )
    )
    user: "User" = Relationship(
        back_populates="user_roles"
    )


class UserBase(SQLModel):
    email: str = Field(
        unique=True,
        description="O e-mail do usuário."
    )
    full_name: str = Field(
        description="O nome completo do usuário."
    )
    cpf: str = Field(
        description="O CPF do usuário."
    )

class User(Base, UserBase, table=True):
    hashed_password: str = Field()
    
    # Relacionamento limpo, apontando apenas para as roles
    user_roles: list["UserRole"] = Relationship(
        back_populates="user"
    )

class UserPublic(UserBase, Base):
    roles: list["RoleEnum"] = Field()

class UserCreate(UserBase):
    roles: list["RoleEnum"] = Field()

class UserUpdate(UserBase):
    roles: list["RoleEnum"] = Field()

class UserList(ListBase):
    users: list["UserPublic"] = Field()