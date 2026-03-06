from mongoengine import connect
import os
from odhbackend.utils.environment_variables import (
    MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASSWORD
)

def init_mongo_db():
    """
    Função chamada apenas UMA VEZ na inicialização do sistema.
    """
    host = 'mongodb' if os.path.exists('/.dockerenv') else MONGO_HOST

    connect(
        db=MONGO_DB,
        host=host,
        port=int(MONGO_PORT),
        username=MONGO_USER,
        password=MONGO_PASSWORD,
        authentication_source="admin"
    )
