import asyncio
import base64

from mailjet_rest import Client

from src.core.config.config import get_settings
from src.modules.core.domain.dtos.email.email_dtos import EmailAttachmentDTO, SendEmailDTO
from src.modules.core.domain.interfaces.iemail_service import IEmailService

settings = get_settings()


class MailjetEmailService(IEmailService):
    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
    ):
        self.api_key = api_key or settings.MAILJET_API_KEY
        self.secret_key = secret_key or settings.MAILJET_SECRET_KEY
        self.from_email = from_email or settings.EMAIL_FROM
        self.from_name = from_name or settings.EMAIL_FROM_NAME

    async def send(self, payload: SendEmailDTO) -> None:
        await asyncio.to_thread(self._send_sync, payload)

    def _send_sync(self, payload: SendEmailDTO) -> None:
        if not self.api_key or not self.secret_key:
            raise ValueError("MAILJET_API_KEY and MAILJET_SECRET_KEY must be configured")
        if not self.from_email:
            raise ValueError("MAILJET_FROM_EMAIL is not configured")

        mailjet = Client(auth=(self.api_key, self.secret_key), version="v3.1")
        data = {"Messages": [self._build_message(payload)]}
        result = mailjet.send.create(data=data)

        if not (200 <= result.status_code < 300):
            raise ValueError(f"Mailjet error: {result.status_code} - {result.json()}")

    def _build_message(self, payload: SendEmailDTO) -> dict:
        message: dict = {
            "From": self._build_from(),
            "To": self._build_recipients(payload.to),
            "Subject": payload.subject,
        }

        if payload.text_body:
            message["TextPart"] = payload.text_body
        if payload.html_body:
            message["HTMLPart"] = payload.html_body
        if payload.cc:
            message["Cc"] = self._build_recipients(payload.cc)
        if payload.bcc:
            message["Bcc"] = self._build_recipients(payload.bcc)
        if payload.reply_to:
            message["ReplyTo"] = {"Email": payload.reply_to}
        if payload.attachments:
            message["Attachments"] = [self._build_attachment(a) for a in payload.attachments]

        return message

    def _build_from(self) -> dict:
        if self.from_name:
            return {"Email": self.from_email, "Name": self.from_name}
        return {"Email": self.from_email}

    def _build_recipients(self, emails: list[str]) -> list[dict]:
        return [{"Email": email} for email in emails]

    def _build_attachment(self, attachment: EmailAttachmentDTO) -> dict:
        return {
            "Filename": attachment.filename,
            "ContentType": attachment.content_type or "application/octet-stream",
            "Base64Content": base64.b64encode(attachment.data).decode("ascii"),
        }
