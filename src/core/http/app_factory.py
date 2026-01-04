import asyncio

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import MetaData
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.errors.base import BaseAppException
from src.core.http.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    sqlalchemy_error_handler,
    sqlalchemy_integrity_handler,
    timeout_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from src.infrastructure.logging.config import configure_logging
from src.modules.core.presentation.http.middlewares.auth_middleware import AuthMiddleware
from src.modules.core.presentation.http.middlewares.request_id import RequestIdMiddleware
from src.modules.core.presentation.http.middlewares.request_logging import RequestLoggingMiddleware
from src.modules.core.presentation.http.routers.auth import auth_router
from src.modules.core.presentation.http.routers.email import email_router
from src.modules.core.presentation.http.routers.users import user_router

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://192.168.15.7:5173",
    "http://192.168.15.6:5173",
    "http://192.168.1.120:4173",
    "http://192.168.1.120:5173",
]

metadata = MetaData()


def create_app() -> FastAPI:
    configure_logging(level="INFO")

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(AuthMiddleware)

    # Middleware (muito comum no mercado): request_id em toda request/response
    app.add_middleware(RequestIdMiddleware)

    # --- Handlers mais comuns ---

    # 1) Suas exceções de aplicação (NotFound, Conflict, etc.)
    app.add_exception_handler(BaseAppException, app_exception_handler)

    # 2) Erros de validação do FastAPI/Pydantic (422)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # 3) HTTPException do Starlette/FastAPI (404, 405, e HTTPException que você lançar)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)

    # 4) Banco de dados (integridade / outros)
    app.add_exception_handler(IntegrityError, sqlalchemy_integrity_handler)  # unique/fk/not-null...
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # conexão/pool/driver...

    # 5) Timeouts (varia conforme como você aplica timeout; registrar ambos é ok)
    app.add_exception_handler(asyncio.TimeoutError, timeout_handler)
    app.add_exception_handler(TimeoutError, timeout_handler)

    # 6) Fallback (500)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Exemplo: registrar suas rotas (separadas)
    # from src.modules.core.interfaces.http.routers.users import router as users_router
    # app.include_router(users_router, prefix="/api")

    app.include_router(auth_router.router)
    app.include_router(email_router.router)
    app.include_router(user_router.router)

    return app
