from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from odhbackend.routers.oauth2_router import oauth2_router
from odhbackend.routers.users_router import users_router
from odhbackend.routers.article_router import articles_router
from odhbackend.services.nosql_data_store_service import init_mongo_db

tags_metadata = [
    {
        "name": "oauth2",
        "description": "Operações de autenticação e geração de tokens JWT."
    },
    {
        "name": "users",
        "description": "Gestão de usuários (Criação, Leitura e Atualização)."
    },
    {
        "name": "Articles Elasticsearch",
        "description": "Busca, paginação e listagem de notícias integradas ao motor Elasticsearch."
    }
]

# Lifespan simplificado
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_mongo_db()
    yield

# Inicialização da aplicação
odhbackend = FastAPI(
    title="OdhBackend - Security Module",
    openapi_tags=tags_metadata, 
    lifespan=lifespan
)

# Configuração de CORS
odhbackend.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Inclusão apenas das rotas de Segurança e Usuários
odhbackend.include_router(router=oauth2_router)
odhbackend.include_router(router=users_router)
odhbackend.include_router(router=articles_router)