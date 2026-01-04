from typing import Optional, cast

from src.modules.core.application.dtos.users.user_dto import UserDTO
from src.modules.core.application.usecases.email.send_email_usecase import SendEmailUseCase
from src.modules.core.domain.dtos.email.email_dtos import SendEmailDTO
from src.modules.core.domain.dtos.users.user_dtos import PayloadCreateUserDTO
from src.modules.core.domain.entities.User import User
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository


class CreateUserUseCase:
    def __init__(self, users_repository: IUsersRepository, send_email_usecase: SendEmailUseCase):
        self.users_repository = users_repository
        self.send_email_usecase = send_email_usecase

    async def execute(self, payload: PayloadCreateUserDTO) -> Optional[UserDTO]:
        created_user = await self.users_repository.create(payload)

        if created_user is None:
            return None

        created_user = cast(User, created_user)

        print("Sending welcome email to:", created_user.email)

        try:
            await self.send_email_usecase.execute(
                SendEmailDTO(
                    to=[created_user.email],
                    subject="Welcome to Our Service!",
                    text_body=f"Hello {created_user.first_name},\n\nThank you for registering at our service. We're excited to have you on board!\n\nBest regards,\nThe Team",
                    html_body=f"<h1>Hello {created_user.first_name},</h1><p>Thank you for registering at our service. We're excited to have you on board!</p><p>Best regards,<br>The Team</p>",
                )
            )
            print("Sent welcome email to:", created_user.email)
        except Exception as e:
            print(f"Failed to send welcome email: {e}")

        return UserDTO(first_name=created_user.first_name, last_name=created_user.last_name, email=created_user.email, active=created_user.active)
