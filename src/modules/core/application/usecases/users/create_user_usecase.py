from typing import Optional, cast

from src.modules.core.application.dtos.users.user_dto import UserDTO
from src.modules.core.domain.dtos.email.email_dtos import SendEmailDTO
from src.modules.core.domain.dtos.users.user_dtos import PayloadCreateUserDTO
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.iemail_service import IEmailService
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository


class CreateUserUseCase:
    def __init__(self, users_repository: IUsersRepository, email_service: IEmailService):
        self.users_repository = users_repository
        self.email_service = email_service

    async def execute(self, payload: PayloadCreateUserDTO) -> Optional[UserDTO]:
        created_user = await self.users_repository.create(payload)

        if created_user is None:
            return None

        created_user = cast(User, created_user)

        print("Sending welcome email to:", created_user.email)

        await self.email_service.send(
            payload=SendEmailDTO(
                to=[created_user.email],
                subject="Welcome to Our Service",
                text_body=f"Hello {created_user.first_name}, welcome to our service!",
                html_body=f"<h1>Hello {created_user.first_name}, welcome to our service!</h1>",
            )
        )

        return UserDTO(first_name=created_user.first_name, last_name=created_user.last_name, email=created_user.email, active=False)
