from typing import Optional, cast

from src.modules.core.application.dtos.users.user_dto import UserDTO
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository


class CreateUserUseCase:
    def __init__(self, users_repository: IUsersRepository):
        self.users_repository = users_repository

    async def execute(self, first_name: str, last_name: str, email: str, password: str, active: bool) -> Optional[UserDTO]:
        user = User(first_name=first_name, last_name=last_name, email=email, password=password, active=active)

        created_user = await self.users_repository.create(user)

        if created_user is None:
            return None

        created_user = cast(User, created_user)

        return UserDTO(first_name=created_user.first_name, last_name=created_user.last_name, email=created_user.email, active=created_user.active)
