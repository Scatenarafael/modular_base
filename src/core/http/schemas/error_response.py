from typing import Any

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = {}


class ErrorResponse(BaseModel):
    error: ErrorBody
    request_id: str | None = None


# {
#   "error": {
#     "code": "CONFLICT",
#     "message": "Email já cadastrado.",
#     "details": {"field": "email"}
#   },
#   "request_id": "..."
# }
