from os import getenv

from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para a memória
load_dotenv(dotenv_path=".env", override=True)

# Segurança e JWT
SECRET_KEY = getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
DEFAULT_USER_PASSWORD = getenv("DEFAULT_USER_PASSWORD")

# Log
LOGGING_LEVEL = getenv("LOGGING_LEVEL")

# Banco de Dados (PostgreSQL)
POSTGRES_HOST = getenv("POSTGRES_HOST")
POSTGRES_PORT = getenv("POSTGRES_PORT")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")