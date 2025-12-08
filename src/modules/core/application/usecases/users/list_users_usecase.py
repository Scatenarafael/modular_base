from typing import List, Optional, cast

from src.modules.core.application.dtos.users.user_dto import UserDTO
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository


class ListUsersUseCase:
    def __init__(self, users_repository: IUsersRepository):
        self.users_repository = users_repository

    async def execute(self) -> Optional[List[UserDTO]]:
        users = await self.users_repository.list()

        if users is None:
            return None

        users = cast(List[User], users)

        casted_users = [UserDTO(first_name=user.first_name, last_name=user.last_name, email=user.email, active=user.active) for user in users]

        return casted_users
