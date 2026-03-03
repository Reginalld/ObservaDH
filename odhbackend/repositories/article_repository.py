import os
from typing import List, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError, ConnectionError

class ArticleRepository:
    def __init__(self):
        """
        Inicializa a conexão com o Elasticsearch.
        Identifica automaticamente se está rodando via Docker ou local.
        """
        my_host = 'elasticsearch_container' if os.path.exists('/.dockerenv') else 'localhost'
        self.client = Elasticsearch([f"http://{my_host}:9200"])
        self.index = "articles"

    def search_articles(
        self,
        any_keywords: Optional[List[str]] = None,
        all_keywords: Optional[List[str]] = None,
        forbidden_keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        from_: int = 0,
        size: int = 25
    ) -> dict:
        """
        Constrói a DSL de busca do Elasticsearch e executa a query.
        """
        query = {"bool": {}}

        # Condição OR (pelo menos uma palavra)
        if any_keywords:
            query["bool"]["should"] = [
                {"match": {"content": {"query": k.lower(), "operator": "or"}}}
                for k in any_keywords
            ]
            query["bool"]["minimum_should_match"] = 1

        # Condição AND (todas as palavras)
        if all_keywords:
            query["bool"]["must"] = [
                {"match": {"content": {"query": k.lower(), "operator": "and"}}}
                for k in all_keywords
            ]

        # Condição NOT (nenhuma das palavras)
        if forbidden_keywords:
            query["bool"]["must_not"] = [
                {"terms": {"content": [k.lower() for k in forbidden_keywords]}}
            ]

        # Filtros exatos (Fonte e Data)
        filters = []
        if source:
            filters.append({"term": {"source": source}})
        
        if start_time or end_time:
            date_filter = {"range": {"timestamp": {}}}
            if start_time:
                date_filter["range"]["timestamp"]["gte"] = start_time
            if end_time:
                date_filter["range"]["timestamp"]["lte"] = end_time
            filters.append(date_filter)

        if filters:
            query["bool"]["filter"] = filters

        try:
            return self.client.search(
                index=self.index,
                query=query,
                from_=from_,
                size=size,
                sort=[{"timestamp": {"order": "desc"}}]
            )
        except (RequestError, ConnectionError) as e:
            print(f"[Elasticsearch Error] Falha na busca: {e}")
            return {}

    def get_article_by_id(self, article_id: str) -> Optional[dict]:
        """
        Busca um documento específico pelo seu ID gerado no Elastic.
        """
        try:
            response = self.client.get(index=self.index, id=article_id)
            return response.get("_source")
        except NotFoundError:
            return None
        except Exception as e:
            print(f"[Elasticsearch Error] Falha ao buscar ID {article_id}: {e}")
            return None