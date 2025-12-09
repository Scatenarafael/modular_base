from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.core.domain.entities.Role import Role
    from src.modules.core.domain.entities.UserCompanyRole import UserCompanyRole


@dataclass
class Company:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""

    users_roles: list[UserCompanyRole] = field(default_factory=list)
    roles: list[Role] = field(default_factory=list)

    def add_role(self, role: Role) -> None:
        self.roles.append(role)
        role.company = self
        role.company_id = self.id

    def add_user_role(self, ucr: UserCompanyRole) -> None:
        self.users_roles.append(ucr)
        ucr.company = self
        ucr.company_id = self.id
