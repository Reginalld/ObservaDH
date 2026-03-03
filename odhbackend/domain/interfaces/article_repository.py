from abc import ABC, abstractmethod
from typing import List, Optional
from odhbackend.models import User

class IArticleRepository(ABC):
    """
    Interface que define o contrato para qualquer repositório de artigos.
    Seguindo o DIP (Dependency Inversion Principle), o Service dependerá 
    desta abstração e não de uma implementação específica (Elastic, Mongo, etc).
    """

    @abstractmethod
    def search(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        skip: int = 0,
        limit: int = 25
    ) -> dict:
        """
        Contrato para busca paginada de artigos.
        """
        pass

    @abstractmethod
    def get_by_id(
        self,
        current_user: User,
        article_id: str
    ) -> Optional[dict]:
        """
        Contrato para recuperar um único artigo pelo seu identificador.
        """
        pass

    @abstractmethod
    def count_by_source(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """
        Contrato para realizar a agregação e contagem de artigos por fonte.
        """
        pass