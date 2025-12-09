from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.core.domain.entities.RefreshToken import RefreshToken
    from src.modules.core.domain.entities.UserCompanyRole import UserCompanyRole


@dataclass
class User:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    hashed_password: str = ""
    active: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Se você quiser refletir os relacionamentos como entidades puras:
    refresh_tokens: list[RefreshToken] = field(default_factory=list)
    companies_roles: list[UserCompanyRole] = field(default_factory=list)
