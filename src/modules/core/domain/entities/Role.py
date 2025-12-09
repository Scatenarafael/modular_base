from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.modules.core.domain.entities.Company import Company
    from src.modules.core.domain.entities.User import User
    from src.modules.core.domain.entities.UserCompanyRole import UserCompanyRole
    from src.modules.core.domain.entities.WorkDay import WorkDay


@dataclass
class Role:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    company_id: Optional[uuid.UUID] = None
    number_of_cooldown_days: int = 0

    company: Optional[Company] = None
    user_company_roles: list[UserCompanyRole] = field(default_factory=list)
    work_days: list[WorkDay] = field(default_factory=list)

    def assign_to_user_in_company(
        self,
        user: User,
        company: Company,
        is_owner: bool = False,
    ) -> UserCompanyRole:
        ucr = UserCompanyRole(
            user_id=user.id,
            company_id=company.id,
            role_id=self.id,
            is_owner=is_owner,
            user=user,
            company=company,
            role=self,
        )
        self.user_company_roles.append(ucr)
        user.companies_roles.append(ucr)
        company.users_roles.append(ucr)
        return ucr
