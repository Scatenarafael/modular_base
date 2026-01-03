from abc import ABC, abstractmethod
from typing import Awaitable

from src.modules.core.domain.dtos.email.email_dtos import SendEmailDTO


class IEmailService(ABC):
    @abstractmethod
    async def send(self, payload: SendEmailDTO) -> Awaitable[None]:
        pass
