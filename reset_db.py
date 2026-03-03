from argparse import ArgumentParser
from os import getenv

from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlmodel import text
from sqlmodel.orm.session import Session
from alembic.config import Config
from alembic import command
from bcrypt import gensalt
from bcrypt import hashpw

from odhbackend.utils.functions import random_string

# 1. Configuração de Argumentos (Local, Develop, Staging)
parser = ArgumentParser()
parser.add_argument("--environment", type=str, default="local")
args = parser.parse_args()

if args.environment == "local":
    load_dotenv(dotenv_path=".env", override=True)
elif args.environment == "develop":
    load_dotenv(dotenv_path=".env.develop", override=True)
elif args.environment == "staging":
    load_dotenv(dotenv_path=".env.staging", override=True)
else:
    load_dotenv(dotenv_path=".env")

# 2. Captura de Variáveis de Ambiente
POSTGRES_HOST = getenv("POSTGRES_HOST")
POSTGRES_PORT = getenv("POSTGRES_PORT")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")

# 3. Criação da Engine do Banco
engine = create_engine(
    url=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# 4. Limpeza Total do Banco (Drop Schema)
print("Limpando schema público...")
with Session(engine) as session:
    session.exec(statement=text(text="DROP SCHEMA IF EXISTS public CASCADE;"
                                     "CREATE SCHEMA public;"))
    session.commit()

# 5. Execução automática do Alembic (Migrações)
print("Rodando migrações do Alembic...")
config = Config(file_="alembic.ini")
config.set_main_option(
    name="sqlalchemy.url",
    value=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
command.upgrade(config=config, revision="head")

# 6. Preparação dos Dados de Usuários (Itaipu Parquetec)
matheus_gonsalves_id = random_string()
thays_achucarro_id = random_string()
neivaldo_moraes_id = random_string()
gustavo_bastos_id = random_string()
paullyanne_farias_id = random_string()
natania_inez_id = random_string()
vitor_marques_id = random_string()

print("Inserindo usuários e roles...")
with Session(engine) as session:
    session.exec(statement=text(text=f"""
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{matheus_gonsalves_id}', 'matheus.gonsalves@itaipuparquetec.org.br', 'Matheus Riquelme Gonsalves', '21795078014', '{hashpw(password=b"secret", salt=gensalt()).decode()}');
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{thays_achucarro_id}', 'thays.achucarro@itaipuparquetec.org.br', 'Thays Resende Achucarro', '68054488084', '{hashpw(password=b"secret", salt=gensalt()).decode()}');
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{neivaldo_moraes_id}', 'neivaldo.moraes@itaipuparquetec.org.br', 'Neivaldo Marcos Dias De Moraes Junior', '49283097076', '{hashpw(password=b"secret", salt=gensalt()).decode()}');
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{gustavo_bastos_id}', 'gustavo.bastos@itaipuparquetec.org.br', 'Gustavo Viana Bastos', '75605068016', '{hashpw(password=b"secret", salt=gensalt()).decode()}');
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{paullyanne_farias_id}', 'paullyanne.farias@itaipuparquetec.org.br', 'Paullyanne Portela de Farias', '37601292002', '{hashpw(password=b"secret", salt=gensalt()).decode()}');
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{natania_inez_id}', 'natania.inez@itaipuparquetec.org.br', 'Natania Pereira Inez', '04143912090', '{hashpw(password=b"secret", salt=gensalt()).decode()}');
INSERT INTO public."user"(
    id, email, full_name, cpf, hashed_password)
    VALUES ('{vitor_marques_id}', 'vitor.marques@itaipuparquetec.org.br', 'Vitor Gabriel Marques Quadros', '75487260079', '{hashpw(password=b"secret", salt=gensalt()).decode()}');

INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{matheus_gonsalves_id}', 'coordination');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{thays_achucarro_id}', 'dpo');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{neivaldo_moraes_id}', 'communication');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{gustavo_bastos_id}', 'indicators');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{paullyanne_farias_id}', 'communication');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{paullyanne_farias_id}', 'indicators');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{natania_inez_id}', 'coordination');
INSERT INTO public."userrole"(
    user_id, role)
    VALUES ('{vitor_marques_id}', 'coordination');
    """))
    session.commit()

print("Ambiente de segurança resetado com sucesso!")