# src/infrastructure/database/mappers/company_mapper.py
from datetime import datetime
from typing import cast
from uuid import UUID

from src.modules.core.domain.entities.RefreshToken import RefreshToken
from src.modules.core.infrastructure.models.refresh_token_model import RefreshTokenModel


class RefreshTokenMapper:
    @staticmethod
    def to_entity(model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=UUID(str(model.id)),
            user_id=UUID(str(model.user_id)),
            token_hash=str(model.token_hash),
            revoked=bool(model.revoked),
            created_at=cast(datetime, model.created_at),
            expires_at=cast(datetime, model.expires_at),
            replaced_by=cast(str | None, model.replaced_by),
        )

    @staticmethod
    def from_entity(entity: RefreshToken) -> RefreshTokenModel:
        # para "create" normalmente você NÃO passa id nem created_at,
        # mas deixo explícito aqui só como exemplo
        return RefreshTokenModel(id=entity.id, user_id=entity.user_id, token_hash=entity.token_hash, created_at=entity.created_at, expires_at=entity.expires_at, revoked=entity.revoked, replaced_by=entity.replaced_by)
