import asyncio
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from src.core.config.config import get_settings
from src.modules.core.domain.dtos.email.email_dtos import EmailAttachmentDTO, SendEmailDTO
from src.modules.core.domain.interfaces.iemail_service import IEmailService

settings = get_settings()


class SmtpEmailService(IEmailService):
    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool | None = None,
        use_ssl: bool | None = None,
        timeout: int | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
    ):
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        self.username = username or settings.EMAIL_USERNAME
        self.password = password or settings.EMAIL_PASSWORD
        self.use_tls = settings.EMAIL_USE_TLS if use_tls is None else use_tls
        self.use_ssl = settings.EMAIL_USE_SSL if use_ssl is None else use_ssl
        self.timeout = timeout or settings.EMAIL_TIMEOUT
        self.from_email = from_email or settings.EMAIL_FROM
        self.from_name = from_name or settings.EMAIL_FROM_NAME

    async def send(self, payload: SendEmailDTO) -> None:
        await asyncio.to_thread(self._send_sync, payload)

    def _send_sync(self, payload: SendEmailDTO) -> None:
        if not self.host:
            raise ValueError("EMAIL_HOST is not configured")
        if not self.from_email:
            raise ValueError("EMAIL_FROM is not configured")

        message = EmailMessage()
        message["Subject"] = payload.subject
        message["From"] = formataddr((self.from_name, self.from_email)) if self.from_name else self.from_email
        message["To"] = ", ".join(payload.to)

        if payload.cc:
            message["Cc"] = ", ".join(payload.cc)
        if payload.reply_to:
            message["Reply-To"] = payload.reply_to

        if payload.text_body and payload.html_body:
            message.set_content(payload.text_body)
            message.add_alternative(payload.html_body, subtype="html")
        elif payload.html_body:
            message.add_alternative(payload.html_body, subtype="html")
        else:
            message.set_content(payload.text_body or "")

        if payload.attachments:
            for attachment in payload.attachments:
                self._add_attachment(message, attachment)

        recipients = payload.to + (payload.cc or []) + (payload.bcc or [])
        smtp_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP

        with smtp_class(self.host, self.port, timeout=self.timeout) as smtp:
            if self.use_tls and not self.use_ssl:
                smtp.starttls()
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(message, from_addr=self.from_email, to_addrs=recipients)

    def _add_attachment(self, message: EmailMessage, attachment: EmailAttachmentDTO) -> None:
        content_type = attachment.content_type or "application/octet-stream"
        if "/" in content_type:
            maintype, subtype = content_type.split("/", 1)
        else:
            maintype, subtype = "application", "octet-stream"
        message.add_attachment(attachment.data, maintype=maintype, subtype=subtype, filename=attachment.filename)
