from random import choice
from datetime import datetime

from string import ascii_letters
from string import digits

from logging import DEBUG
from logging import INFO
from logging import WARNING
from logging import ERROR
from logging import CRITICAL
from logging import Logger
from logging import getLogger
from logging import FileHandler
from logging import Formatter

# Removido: odhbackend.documents (Elasticsearch)
from odhbackend.utils.environment_variables import LOGGING_LEVEL


def random_string() -> str:
    return "".join(choice(
        ascii_letters + digits
    ) for _ in range(22))


def is_valid_id(id_to_validate: str) -> bool:
    if not id_to_validate:
        return False
    if len(id_to_validate) != 22:
        return False
    return all(char in ascii_letters + digits for char in id_to_validate)


def get_logger(name: str) -> Logger:
    logger = getLogger(name=name)
    # Define o nível baseado no .env
    if LOGGING_LEVEL == "DEBUG":
        logger.setLevel(level=DEBUG)
    elif LOGGING_LEVEL == "INFO":
        logger.setLevel(level=INFO)
    elif LOGGING_LEVEL == "WARNING":
        logger.setLevel(level=WARNING)
    elif LOGGING_LEVEL == "ERROR":
        logger.setLevel(level=ERROR)
    elif LOGGING_LEVEL == "CRITICAL":
        logger.setLevel(level=CRITICAL)
    
    file_handler = FileHandler(
        filename=f"./odhbackend/logs/{name}.log",
        encoding="utf-8"
    )
    formatter = Formatter(
        fmt=f"%(asctime)s [{name}] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(fmt=formatter)
    logger.addHandler(hdlr=file_handler)
    return logger


def log(
        level: str,
        message: str,
        where: str,
        module_name: str,
        status_code: int = 0,
        detail: str = ""
):
    log_dict = dict(
        logged_on=datetime.now(),
        level=level,
        status_code=status_code,
        message=message,
        detail=detail,
        where=where
    )
    
    # Como removemos o Elasticsearch, agora o log principal vai para o arquivo
    try:
        msg = f"[{where}] {message} | Status: {status_code} | Detail: {detail}"
        logger = get_logger(name=module_name)
        
        if level == "DEBUG": logger.debug(msg)
        elif level == "INFO": logger.info(msg)
        elif level == "WARNING": logger.warning(msg)
        elif level == "ERROR": logger.error(msg)
        elif level == "CRITICAL": logger.critical(msg)
        
    except Exception as e:
        # Fallback de erro no próprio sistema de log
        print(f"Erro ao registrar log: {e} {log_dict}")