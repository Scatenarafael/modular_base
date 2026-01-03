from dataclasses import dataclass


@dataclass
class EmailAttachmentDTO:
    filename: str
    content_type: str
    data: bytes


@dataclass
class SendEmailDTO:
    to: list[str]
    subject: str
    text_body: str | None = None
    html_body: str | None = None
    cc: list[str] | None = None
    bcc: list[str] | None = None
    reply_to: str | None = None
    attachments: list[EmailAttachmentDTO] | None = None
