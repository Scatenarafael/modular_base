from fastapi import APIRouter, Depends, HTTPException, status

from src.modules.core.application.usecases.email.send_email_usecase import SendEmailUseCase
from src.modules.core.presentation.http.routers.email.utils import get_send_email_usecase
from src.modules.core.presentation.http.schemas.dtos.email_dto import SendEmailPayloadDTO
from src.modules.core.presentation.http.schemas.pydantic.email_schema import SendEmailRequestBody

router = APIRouter(tags=["email"], prefix="/email")


@router.post("/send", status_code=status.HTTP_202_ACCEPTED)
async def send_email(payload: SendEmailRequestBody, send_email_usecase: SendEmailUseCase = Depends(get_send_email_usecase)):
    try:
        await send_email_usecase.execute(SendEmailPayloadDTO().to_usecase(payload))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"message": "Email accepted for delivery"}


# {
#   "to": ["destinatario@exemplo.com"],
#   "subject": "Teste de envio",
#   "text_body": "Olá! Este é um teste de envio de email.",
#   "html_body": "<p>Olá! Este é um <strong>teste</strong> de envio de email.</p>",
#   "cc": ["copia@exemplo.com"],
#   "bcc": ["oculto@exemplo.com"],
#   "reply_to": "responder@exemplo.com"
# }
