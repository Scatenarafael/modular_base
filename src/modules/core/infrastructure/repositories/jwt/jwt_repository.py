from datetime import datetime
from typing import Optional

from sqlalchemy import select, update

from src.infrastructure.database.settings.connection import DbConnectionHandler
from src.modules.core.domain.entities.RefreshToken import RefreshToken
from src.modules.core.domain.interfaces.ijwt_repository import IJWTRepository
from src.modules.core.infrastructure.mappers.refresh_token_mapper import RefreshTokenMapper
from src.modules.core.infrastructure.models.refresh_token_model import RefreshTokenModel


class JWTRepository(IJWTRepository):
    @classmethod
    async def save_refresh_token(cls, jti: str, user_id: str, token_hash: str, expires_at: datetime) -> Optional[RefreshToken]:
        async with DbConnectionHandler() as database:
            new_register = RefreshTokenModel(id=jti, user_id=user_id, token_hash=token_hash, expires_at=expires_at)

            if not new_register:
                raise ValueError("Could not save refresh_token")
            try:
                if database.session:
                    database.session.add(new_register)
                    await database.session.commit()
                    await database.session.refresh(new_register)
                    refresh_token = RefreshTokenMapper.to_entity(new_register)
                    return refresh_token
            except Exception as exception:
                raise exception

    @classmethod
    async def get_by_jti(cls, jti: str) -> Optional[RefreshToken]:
        async with DbConnectionHandler() as database:
            try:
                if database.session:
                    stmt = select(RefreshTokenModel).where(RefreshTokenModel.id == jti)
                    result = await database.session.scalars(stmt)
                    rt = result.first()
                    if not rt:
                        raise LookupError("RefreshToken not found!")
                    refresh_token = RefreshTokenMapper.to_entity(rt)
                    return refresh_token
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception

    @classmethod
    async def revoke_token(cls, token: RefreshToken, replaced_by: str | None = None) -> Optional[RefreshToken]:
        token.revoked = True
        if replaced_by:
            token.replaced_by = replaced_by

        async with DbConnectionHandler() as database:
            try:
                token_model = RefreshTokenMapper.from_entity(token)
                if not token_model:
                    raise ValueError("Could not save refresh_token")

                if database.session:
                    database.session.add(token_model)
                    await database.session.commit()
                    return token
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception

    @classmethod
    async def delete_token(cls, token: RefreshToken):
        async with DbConnectionHandler() as database:
            try:
                token_model = RefreshTokenMapper.from_entity(token)
                if database.session:
                    await database.session.delete(token_model)
                    await database.session.commit()
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception

    @classmethod
    async def revoke_all_for_user(cls, user_id: str):
        async with DbConnectionHandler() as database:
            try:
                if database.session:
                    stmt = update(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id, RefreshTokenModel.revoked.is_(False)).values(revoked=True)
                    await database.session.execute(stmt)
                    await database.session.commit()
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception
