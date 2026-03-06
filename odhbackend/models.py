from typing import Optional, List
import enum
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship, Enum, Column, UniqueConstraint


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

    keyword_lists: list["KeywordList"] = Relationship(back_populates="owner")

class UserPublic(UserBase, Base):
    roles: list["RoleEnum"] = Field()

class UserCreate(UserBase):
    roles: list["RoleEnum"] = Field()

class UserUpdate(UserBase):
    roles: list["RoleEnum"] = Field()

class UserList(ListBase):
    users: list["UserPublic"] = Field()

class Comment(SQLModel):
    """Representa um comentário no artigo"""
    user: str
    comment: str
    position: Optional[int] = None

class Article(SQLModel):
    id: Optional[str] = Field(default=None, primary_key=True) 
    link: str
    
    userId: str = ""
    keyword: Optional[str] = "geral" 
    source: Optional[str] = "Desconhecida"
    language: Optional[str] = "pt"
    title: Optional[str] = "Sem Título"
    content: Optional[str] = None
    
    comments: List[dict] = [] 
    images: List[dict] = [] 
    
    hash: Optional[str] = None
    timestamp: Optional[str] = None

    @field_validator("keyword", mode="before")
    @classmethod
    def ensure_keyword_is_string(cls, value):
        if not isinstance(value, str) or value is None:
            return "geral"
        return value

class PaginatedArticleResponse(SQLModel):
    """Resposta padrão para o Feed"""
    articles: List[Article]
    total: int
    page: int
    size: int
    total_pages: int

class Comments(SQLModel):
    user: Optional[str] = None
    comment: Optional[str] = None
    position: Optional[int] = None

class Images(SQLModel):
    articleposition: str # Conforme o seu original: String!
    image: str
    caption: str

class KeywordList(SQLModel, table=True):
    __tablename__ = "keyword_list"

    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str = Field(index=True, max_length=255)
    
    user_id: str = Field(foreign_key="user.id")

    # Relacionamento de volta para o usuário
    owner: Optional["User"] = Relationship(back_populates="keyword_lists")

    __table_args__ = (
        UniqueConstraint('user_id', 'keyword', name='user_keyword_uc'),
    )
