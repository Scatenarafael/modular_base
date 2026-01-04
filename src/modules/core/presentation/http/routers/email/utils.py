from src.infrastructure.external_services.email_service.mailjet_email_service import MailjetEmailService
from src.modules.core.application.usecases.email.send_email_usecase import SendEmailUseCase


def get_send_email_usecase():
    return SendEmailUseCase(MailjetEmailService(from_email="rafascatena@gmail.com", from_name="Scatena Delivery"))
