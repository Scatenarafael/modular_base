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


# data = {
#   'Messages': [
# 				{
# 						"From": {
# 								"Email": "pilot@mailjet.com",
# 								"Name": "Mailjet Pilot"
# 						},
# 						"To": [
# 								{
# 										"Email": "passenger1@mailjet.com",
# 										"Name": "passenger 1"
# 								}
# 						],
# 						"Subject": "Your email flight plan!",
# 						"TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
# 						"HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
# 				}
# 		]
# }
