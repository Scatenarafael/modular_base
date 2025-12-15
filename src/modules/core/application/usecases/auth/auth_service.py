import hmac
import uuid
from datetime import datetime, timedelta, timezone
from typing import cast

from src.core.config.config import get_settings
from src.modules.core.application.usecases.auth.utils import InvalidCredentials, RefreshExpired, RefreshInvalid, RefreshReuseDetected
from src.modules.core.domain.entities.RefreshToken import RefreshToken
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.ijwt_repository import IJWTRepository
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository
from src.modules.core.infrastructure.repositories.jwt.security import create_access_token, generate_refresh_token_raw, hash_refresh_token, verify_access_token

settings = get_settings()


class AuthService:
    def __init__(self, user_repo: IUsersRepository, token_repo: IJWTRepository):
        # instancing required repositories
        self.user_repo = user_repo
        self.token_repo = token_repo

    # creating new jti
    def _new_jti(self) -> str:
        return str(uuid.uuid4())

    # validating user and password, returning access and refresh tokens
    async def login(self, email: str, password: str):
        # Initial authentication
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentials("Invalid email or password")

        user = cast(User, user)

        is_password_valid = self.user_repo.verify_password(password, user.hashed_password)

        if not is_password_valid:
            raise InvalidCredentials("Invalid email or password")

        # creating access token
        access = create_access_token(str(user.id))

        # creating refresh token
        raw_refresh = generate_refresh_token_raw()
        refresh_hash = hash_refresh_token(raw_refresh)

        jti = self._new_jti()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        await self.token_repo.save_refresh_token(
            jti=jti,
            user_id=str(user.id),
            token_hash=refresh_hash,
            expires_at=expires_at,
        )

        return {"access_token": access, "refresh_token": raw_refresh, "refresh_jti": jti, "user_id": str(user.id)}

    async def rotate_refresh(self, raw_refresh: str, jti: str):
        # refreshing token
        record_model = await self.token_repo.get_by_jti(jti)

        if not record_model:
            raise InvalidCredentials("Refresh token não encontrado")

        record_model = cast(RefreshToken, record_model)

        if record_model.revoked:
            # recicling detected → lets revolke this user chain
            await self.token_repo.revoke_all_for_user(str(record_model.user_id))
            raise RefreshReuseDetected("Refresh reutilizado. Sessões revogadas.")

        # validates the hash securely
        if not hmac.compare_digest(record_model.token_hash, hash_refresh_token(raw_refresh)):
            await self.token_repo.revoke_all_for_user(str(record_model.user_id))
            raise RefreshInvalid("Refresh inválido. Sessões revogadas.")

        expires_at = record_model.expires_at if isinstance(record_model.expires_at, datetime) else datetime.fromisoformat(record_model.expires_at)

        if expires_at < datetime.now(timezone.utc):
            raise RefreshExpired("Refresh expirado")

        # revokes old refresh token
        await self.token_repo.revoke_all_for_user(str(record_model.user_id))
        # await self.token_repo.revoke_token(record_model, replaced_by=new_jti)

        # recicling should be done only if refresh_token is valid and not expired
        new_raw = generate_refresh_token_raw()
        new_hash = hash_refresh_token(new_raw)
        new_jti = self._new_jti()
        new_expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        # saving new refresh token
        await self.token_repo.save_refresh_token(
            jti=new_jti,
            user_id=str(record_model.user_id),
            token_hash=new_hash,
            expires_at=new_expires,
        )

        # new access token
        new_access = create_access_token(str(record_model.user_id))

        return {
            "access_token": new_access,
            "refresh_token": new_raw,
            "refresh_jti": new_jti,
            "user_id": str(record_model.user_id),
        }

    async def logout_by_cookie(self, raw_refresh: str, jti: str) -> bool:
        rec = await self.token_repo.get_by_jti(jti)

        rec = cast(RefreshToken, rec)

        if rec and hmac.compare_digest(rec.token_hash, hash_refresh_token(raw_refresh)):
            await self.token_repo.revoke_token(rec)
            return True
        return False

    async def return_user_by_access_token(self, access_token: str):
        payload = verify_access_token(access_token)

        if not payload:
            raise InvalidCredentials("Token is not valid")

        user_id = payload.get("sub")

        if not user_id:
            raise InvalidCredentials("Token is not valid")

        user = await self.user_repo.get_by_id(user_id)

        user = cast(User, user)

        if hasattr(user, "hashed_password"):
            delattr(user, "hashed_password")  # remove hashed_password before returning

        print("user:", user)
        return user
