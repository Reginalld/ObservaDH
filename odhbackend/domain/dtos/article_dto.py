from pydantic import BaseModel
from typing import List, Optional, Any

class ArticleDTO(BaseModel):
    id: str
    content: str
    source: str
    link: str
    timestamp: str

class PaginatedArticleResponse(BaseModel):
    articles: List[ArticleDTO]
    total: int
    page: int
    size: int
    total_pages: int