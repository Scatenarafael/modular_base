from typing import Any


class BaseAppException(Exception):
    code: str = "APP_ERROR"
    status_code: int = 400

    def __init__(self, message: str, *, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
