from typing import Optional, cast

from src.modules.core.application.dtos.users.user_dto import UserDTO
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository


class RetrieveUserUseCase:
    def __init__(self, users_repository: IUsersRepository):
        self.users_repository = users_repository

    async def execute(self, user_id: str) -> Optional[UserDTO]:
        user = await self.users_repository.get_by_id(user_id)

        if user is None:
            return None

        user = cast(User, user)

        return UserDTO(first_name=user.first_name, last_name=user.last_name, email=user.email, active=user.active)
