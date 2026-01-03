from src.modules.core.domain.dtos.email.email_dtos import SendEmailDTO
from src.modules.core.domain.interfaces.iemail_service import IEmailService


class SendEmailUseCase:
    def __init__(self, email_service: IEmailService):
        self.email_service = email_service

    async def execute(self, payload: SendEmailDTO) -> None:
        self._validate_payload(payload)
        await self.email_service.send(payload)

    def _validate_payload(self, payload: SendEmailDTO) -> None:
        if not payload.to:
            raise ValueError("Email must have at least one recipient")
        if not payload.subject.strip():
            raise ValueError("Email subject cannot be empty")
        if not payload.text_body and not payload.html_body:
            raise ValueError("Email must have a text or HTML body")
