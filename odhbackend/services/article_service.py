import base64
import hashlib
from datetime import datetime, timezone
from io import BytesIO
from PIL import Image
from typing import List, Optional
from sqlalchemy.orm import Session

from odhbackend.models import User, Article
from odhbackend.domain.interfaces.article_repository import IArticleRepository
from odhbackend.services.keyword_service import KeyWordsServices
from odhbackend.models_mongo import ImagesModel

MAX_IMAGES_PER_ARTICLE = 5

class ArticleService:
    """
    Serviço de Artigos que coordena a lógica de negócio.
    Ele depende da interface IArticleRepository e não do Elastic diretamente.
    """

    def __init__(self, repository: IArticleRepository, db: Session) -> None:
        self.repository = repository
        self.db = db

    def _get_images_bulk(self, document_ids: List[str], thumb: bool = False) -> dict:
        """Busca imagens de vários artigos de uma vez no MongoDB"""
        try:
            images = ImagesModel.objects(elasticid__in=document_ids)
            result = {}
            
            for img in images:
                key = img.elasticid
                if key not in result:
                    result[key] = []
                
                if len(result[key]) < MAX_IMAGES_PER_ARTICLE:
                    result[key].append({
                        "articleposition": img.articleposition,
                        "image": img.thumb_sd if thumb else img.image,
                        "caption": img.caption
                    })
            
            return result
        except Exception as e:
            print(f"Erro ao buscar imagens em lote: {e}")
            return{}

    def _get_fallback_keywords(self, user_id: str, provided_keywords: Optional[List[str]]) -> Optional[List[str]]:
        """Se o usuário não passar keywords, pega as da lista geral dele."""
        if not provided_keywords:
            keywords_service = KeyWordsServices(self.db)
            return keywords_service.get_keywords_for_user(user_id=user_id)
        return provided_keywords

    def get_paginated_feed(self, current_user: User, page: int = 1, **kwargs) -> dict:
        any_k = self._get_fallback_keywords(current_user.id, kwargs.get('any_keywords'))
        
        size = 25
        skip = (page - 1) * size if page >= 1 else 0

        exclude_keys = {'any_keywords', 'page', 'size'}
        clean_kwargs = {k: v for k, v in kwargs.items() if k not in exclude_keys}

        raw_result = self.repository.search(
            current_user=current_user,
            any_keywords=any_k,
            skip=skip,
            limit=size,
            **clean_kwargs
        )

        hits_data = raw_result.get("hits", {})
        total_results = hits_data.get("total", {}).get("value", 0)
        hits = hits_data.get("hits", [])

        doc_ids = [hit["_id"] for hit in hits]
        images_map = self._get_images_bulk(doc_ids, thumb=False)

        articles = []
        for hit in hits:
            doc_id = hit["_id"]
            data = hit["_source"]
            
            data["images"] = images_map.get(doc_id, [])
            data.pop("id", None) # Evita o erro de 'multiple values for id'
            
            articles.append(Article(id=doc_id, **data))

        return {
            "articles": articles,
            "total": total_results,
            "page": page,
            "size": size,
            "total_pages": (total_results + size - 1) // size if size > 0 else 0,
        }

    def get_article_detail(self, current_user: User, article_id: str) -> dict:
        """AR02: Detalhe fiel ao original"""
        article_source = self.repository.get_by_id(current_user, article_id)
        
        if not article_source:
            return {"status": "error", "message": "Artigo não encontrado."}
        
        images = self._get_images_bulk([article_id], thumb=False)
        article_source["images"] = images.get(article_id, [])

        article_source.pop("id", None)
        
        return {"status": "success", "data": Article(id=article_id, **article_source)}
    
    def search_full(self, current_user: User, **kwargs) -> dict:
        """AR03: Busca geral de artigos (sem paginação estrita)."""
        final_any_keywords = self._get_fallback_keywords(current_user.id, kwargs.get('any_keywords'))

        raw_result = self.repository.search(
            current_user=current_user,
            any_keywords=final_any_keywords,
            skip=0,
            limit=100,
            **{k: v for k, v in kwargs.items() if k != 'any_keywords'}
        )

        hits = raw_result.get("hits", {}).get("hits", [])
        doc_ids = [hit["_id"] for hit in hits]
        images_map = self._get_images_bulk(doc_ids, thumb=False)

        articles = []
        for hit in hits:
            doc_id = hit["_id"]
            data = hit["_source"]
            
            data["images"] = images_map.get(doc_id, [])
            
            data.pop("id", None)
            articles.append(Article(id=doc_id, **data))

        return {"articles": articles}

    def get_sources_aggregation(
        self,
        current_user: User,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> dict:
        """
        AR04: Processa a agregação de fontes do Elasticsearch.
        """
        final_any_keywords = self._get_fallback_keywords(current_user.email, any_keywords)

        raw_result = self.repository.count_by_source(
            current_user=current_user,
            any_keywords=final_any_keywords,
            all_keywords=all_keywords,
            forbidden_keywords=forbidden_keywords,
            start_time=start_time,
            end_time=end_time
        )
        
        buckets = raw_result.get("aggregations", {}).get("sources", {}).get("buckets", [])
        
        formatted_sources = [{b["key"]: b["doc_count"] for b in buckets}]

        return {"sources": formatted_sources}

    def _generate_sd_thumb(self, base64_str: str, size=(640, 360)) -> str:
        """Gera a miniatura da imagem usando a biblioteca PIL."""
        try:
            image_data = base64.b64decode(base64_str)
            image = Image.open(BytesIO(image_data))
            image.thumbnail(size)
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception:
            return ""

    def index_document(self, article: Article) -> dict:
        """Processo de Ingestão: Hash -> Mongo -> Elastic"""
        link = article.link.strip()
        if not link:
            raise ValueError("O campo 'link' não pode estar vazio.")

        doc_id = hashlib.sha256(link.encode('utf-8')).hexdigest()

        if article.images:
            for img_data in article.images:
                try:
                    thumb = self._generate_sd_thumb(img_data.get('image', ''))
                    
                    ImagesModel(
                        elasticid=doc_id,
                        articleposition=str(img_data.get('articleposition', '0')),
                        image=img_data.get('image', ''),
                        caption=img_data.get('caption', ''),
                        thumb_sd=thumb,
                    ).save()
                except Exception as e:
                    print(f"Erro ao salvar imagem no MongoDB: {e}")

        doc_dict = article.model_dump(exclude={'images'}) if hasattr(article, 'model_dump') else article.dict(exclude={'images'})
        
        doc_dict.update({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hash": doc_id
        })
        
        return self.repository.index(doc_id=doc_id, document=doc_dict)