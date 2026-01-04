# src/infrastructure/database/exceptions.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class DatabaseError(Exception):
    """Erro base de banco (infra)."""


class DatabaseUnavailable(DatabaseError):
    """DB fora/indisponível (conexão, pool, etc.)."""


class DatabaseIntegrityError(DatabaseError):
    """Violação de integridade genérica."""


class UniqueViolation(DatabaseIntegrityError):
    """Violação de constraint UNIQUE."""


class ForeignKeyViolation(DatabaseIntegrityError):
    """Violação de constraint FOREIGN KEY."""


@dataclass(frozen=True)
class IntegrityInfo:
    kind: str  # "unique" | "fk" | "other"
    pgcode: Optional[str]
    message: str


def parse_integrity_error(exc: IntegrityError) -> IntegrityInfo:
    """
    Tenta identificar o tipo de violação de integridade.
    Funciona bem com:
      - postgresql+asyncpg (orig costuma ter classes como UniqueViolationError)
      - psycopg/psycopg2 (orig pode ter pgcode 23505/23503)
    """
    orig = getattr(exc, "orig", None)
    pgcode = getattr(orig, "pgcode", None)

    orig_name = orig.__class__.__name__ if orig else ""
    msg = str(orig) if orig else str(exc)
    msg_low = msg.lower()

    # asyncpg
    if orig_name == "UniqueViolationError":
        return IntegrityInfo(kind="unique", pgcode=pgcode, message=msg)
    if orig_name == "ForeignKeyViolationError":
        return IntegrityInfo(kind="fk", pgcode=pgcode, message=msg)

    # psycopg/psycopg2 postgres codes
    # 23505 = unique_violation
    if pgcode == "23505":
        return IntegrityInfo(kind="unique", pgcode=pgcode, message=msg)
    # 23503 = foreign_key_violation
    if pgcode == "23503":
        return IntegrityInfo(kind="fk", pgcode=pgcode, message=msg)

    # fallback por texto
    if "unique" in msg_low or "duplicate" in msg_low:
        return IntegrityInfo(kind="unique", pgcode=pgcode, message=msg)
    if "foreign key" in msg_low:
        return IntegrityInfo(kind="fk", pgcode=pgcode, message=msg)

    return IntegrityInfo(kind="other", pgcode=pgcode, message=msg)


def wrap_sqlalchemy_error(exc: Exception) -> DatabaseError:
    """
    Converte exceções do SQLAlchemy em exceções de infra do seu projeto.
    Use no repositório/infra (não no domínio).
    """
    if isinstance(exc, IntegrityError):
        info = parse_integrity_error(exc)
        if info.kind == "unique":
            return UniqueViolation(info.message)
        if info.kind == "fk":
            return ForeignKeyViolation(info.message)
        return DatabaseIntegrityError(info.message)

    if isinstance(exc, SQLAlchemyError):
        return DatabaseUnavailable(str(exc))

    return DatabaseError(str(exc))
