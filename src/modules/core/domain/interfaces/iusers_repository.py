from abc import ABC, abstractmethod
from typing import Awaitable, Optional
from uuid import UUID

from src.modules.core.domain.entities.User import User
from src.modules.core.infrastructure.mappers.user_mapper import PayloadUpdateUser


class IUsersRepository(ABC):
    @abstractmethod
    async def list(self) -> Awaitable[list[User] | None]:
        pass

    @abstractmethod
    async def create(self, user: User) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def partial_update_by_id(self, id: UUID, payload: PayloadUpdateUser) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> Awaitable[None]:
        pass

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        pass
