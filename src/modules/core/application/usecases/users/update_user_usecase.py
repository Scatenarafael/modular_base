from typing import cast
from uuid import UUID

from src.modules.core.application.dtos.users.user_dto import UserDTO
from src.modules.core.domain.dtos.users.user_dtos import PayloadUpdateUserDTO
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository


class UpdateUserUseCase:
    def __init__(self, users_repository: IUsersRepository):
        self.users_repository = users_repository

    async def execute(self, user_id: str, payload: PayloadUpdateUserDTO):
        user = await self.users_repository.partial_update_by_id(id=UUID(user_id), payload=payload)

        updated_user = cast(User, user)

        return UserDTO(first_name=updated_user.first_name, last_name=updated_user.last_name, email=updated_user.email, active=updated_user.active)
