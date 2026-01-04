from src.infrastructure.external_services.email_service.mailjet_email_service import MailjetEmailService
from src.modules.core.application.usecases.email.send_email_usecase import SendEmailUseCase


def get_email_service() -> MailjetEmailService:
    return MailjetEmailService()


def get_send_email_usecase() -> SendEmailUseCase:
    return SendEmailUseCase(email_service=get_email_service())
