from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.modules.core.domain.entities.user import User


@dataclass
class RefreshToken:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID | None = None
    token_hash: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revoked: bool = False
    replaced_by: Optional[str] = None

    # Relacionamento de domínio
    user: Optional[User] = None

    def revoke(self, *, replaced_by: str | None = None) -> None:
        self.revoked = True
        self.replaced_by = replaced_by

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at
