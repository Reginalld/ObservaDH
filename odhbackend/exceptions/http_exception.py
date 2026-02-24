from typing import Optional
import fastapi
from fastapi import status
# Removido: elastic_transport (ConnectionTimeout)
from odhbackend.utils.functions import log
from odhbackend.utils.functions import get_logger


class HTTPException:
    @staticmethod
    def raise_http_exception(
            logging_level: str,
            status_code: int,
            message: str,
            detail: str,
            where: str
    ) -> fastapi.HTTPException:
        log(
            level=logging_level,
            message=message,
            where=where,
            module_name="exceptions",
            status_code=status_code,
            detail=detail
        )
        raise fastapi.HTTPException(
            status_code=status_code,
            detail=message
        )

    @staticmethod
    def raise_bad_request(
            message: str,
            detail: Optional[str] = "null",
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        HTTPException.raise_http_exception(
            logging_level="ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            detail=detail,
            where=where
        )

    @staticmethod
    def raise_unauthorized(
            message: Optional[str] = "Não autorizado.",
            detail: Optional[str] = "null",
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        HTTPException.raise_http_exception(
            logging_level="ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            detail=detail,
            where=where
        )

    @staticmethod
    def raise_forbidden(
            message: Optional[str] = "Permissões insuficientes.",
            detail: Optional[str] = "null",
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        HTTPException.raise_http_exception(
            logging_level="ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            detail=detail,
            where=where
        )

    @staticmethod
    def raise_not_found(
            message: Optional[str] = "Não encontrado.",
            detail: Optional[str] = "null",
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        HTTPException.raise_http_exception(
            logging_level="DEBUG",
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            detail=detail,
            where=where
        )

    @staticmethod
    def raise_request_timeout(
            message: Optional[str] = "Tempo limite da requisição.",
            detail: Optional[str] = "null",
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        HTTPException.raise_http_exception(
            logging_level="ERROR",
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            message=message,
            detail=detail,
            where=where
        )

    @staticmethod
    def raise_conflict(
            message: Optional[str] = "Conflito.",
            detail: Optional[str] = "null",
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        HTTPException.raise_http_exception(
            logging_level="ERROR",
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            detail=detail,
            where=where
        )

    @staticmethod
    def raise_internal_server_error(
            e,
            where: Optional[str] = "null"
    ) -> fastapi.HTTPException:
        if isinstance(e, fastapi.HTTPException):
            raise e
        else:
            HTTPException.raise_http_exception(
                logging_level="ERROR",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Erro interno do servidor.",
                detail=str(e),
                where=where
            )