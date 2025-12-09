from abc import ABC, abstractmethod
from typing import Awaitable, Optional
from uuid import UUID

from src.modules.core.domain.dtos.users.user_dtos import PayloadCreateUserDTO, PayloadUpdateUserDTO
from src.modules.core.domain.entities.User import User


class IUsersRepository(ABC):
    @abstractmethod
    async def list(self) -> Awaitable[list[User] | None]:
        pass

    @abstractmethod
    async def create(self, payload: PayloadCreateUserDTO) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def partial_update_by_id(self, id: UUID, payload: PayloadUpdateUserDTO) -> Awaitable[Optional[User]]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> Awaitable[None]:
        pass

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        pass
