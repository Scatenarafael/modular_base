from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from src.modules.core.domain.entities.Company import Company
from src.modules.core.domain.entities.Role import Role
from src.modules.core.domain.entities.user import User


@dataclass
class UserCompanyRole:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    role_id: Optional[uuid.UUID] = None
    is_owner: bool = False

    user: Optional[User] = None
    company: Optional[Company] = None
    role: Optional[Role] = None

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "company_id": str(self.company_id) if self.company_id else None,
            "role_id": str(self.role_id) if self.role_id else None,
            "is_owner": self.is_owner,
        }
