import asyncio
import logging
from typing import cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from src.core.errors.app import Conflict, ServiceUnavailable
from src.core.errors.base import BaseAppException

logger = logging.getLogger("app")


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None) or request.headers.get("x-request-id")


def _json_error(
    status_code: int,
    code: str,
    message: str,
    request_id: str | None,
    details: dict | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            },
            "request_id": request_id,
        },
    )


async def app_exception_handler(request: Request, exc: Exception) -> Response:
    exc_ = cast(BaseAppException, exc)
    return _json_error(exc_.status_code, exc_.code, exc_.message, _request_id(request), exc_.details)


async def validation_exception_handler(request: Request, exc: Exception) -> Response:
    exc_ = cast(RequestValidationError, exc)
    return _json_error(
        422,
        "VALIDATION_ERROR",
        "Dados inválidos.",
        _request_id(request),
        {"errors": exc_.errors()},
    )


async def http_exception_handler(request: Request, exc: Exception) -> Response:
    exc_ = cast(StarletteHTTPException, exc)
    detail = exc_.detail if isinstance(exc_.detail, str) else "Erro na requisição."
    return _json_error(exc_.status_code, "HTTP_ERROR", detail, _request_id(request))


def _is_unique_violation_from_integrity_error(exc: IntegrityError) -> bool:
    orig = getattr(exc, "orig", None)
    name = orig.__class__.__name__ if orig else ""

    if name == "UniqueViolationError":
        return True

    pgcode = getattr(orig, "pgcode", None)
    if pgcode == "23505":
        return True

    msg = str(orig) if orig else ""
    return "unique" in msg.lower() or "duplicate" in msg.lower()


async def sqlalchemy_integrity_handler(request: Request, exc: Exception) -> Response:
    exc_ = cast(IntegrityError, exc)

    if _is_unique_violation_from_integrity_error(exc_):
        mapped = Conflict("Conflito de dados (valor já existe).")
        return await app_exception_handler(request, mapped)

    return _json_error(409, "INTEGRITY_ERROR", "Conflito/violação de integridade.", _request_id(request))


async def sqlalchemy_error_handler(request: Request, exc: Exception) -> Response:
    logger.exception("SQLAlchemyError", extra={"request_id": _request_id(request)})
    mapped = ServiceUnavailable("Banco de dados indisponível no momento.")
    return await app_exception_handler(request, mapped)


async def timeout_handler(request: Request, exc: Exception) -> Response:
    mapped = ServiceUnavailable("Tempo excedido ao processar a requisição.")
    return await app_exception_handler(request, mapped)


async def unhandled_exception_handler(request: Request, exc: Exception) -> Response:
    if isinstance(exc, asyncio.CancelledError):
        raise exc  # <- precisa ser raise exc (não raise “sozinho”)

    logger.exception("Unhandled exception", extra={"request_id": _request_id(request)})
    return _json_error(500, "INTERNAL_SERVER_ERROR", "Ocorreu um erro inesperado.", _request_id(request))
