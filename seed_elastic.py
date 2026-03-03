from elasticsearch import Elasticsearch
from datetime import datetime, timezone

es = Elasticsearch(["http://localhost:9200"])
index_name = "articles"

noticias = [
    {
        "link": "https://g1.globo.com/noticia1",
        "content": "Itaipu bate recorde de geração de energia limpa neste mês.",
        "source": "G1",
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "link": "https://cnnbrasil.com.br/noticia2",
        "content": "Novo projeto no Parquetec utiliza imagens de satélites Sentinel para inteligência territorial.",
        "source": "CNN",
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "link": "https://techcrunch.com/noticia3",
        "content": "Empresas de tecnologia investem pesado em infraestrutura de dados geoespaciais e Docker.",
        "source": "TechCrunch",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
]

print("Injetando dados no Elasticsearch...")
for i, doc in enumerate(noticias):
    es.index(index=index_name, id=f"teste_{i+1}", document=doc)

print("notícias injetadas com sucesso!")