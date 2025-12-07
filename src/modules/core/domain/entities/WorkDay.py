from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.modules.core.domain.entities.Role import Role
from src.modules.core.domain.entities.WorkShift import WorkShift


@dataclass
class WorkDay:
    # no domínio, id pode ser None até ser persistido
    id: Optional[int] = None
    role_id: Optional[uuid.UUID] = None
    weekday: Optional[int] = None  # 0 = Monday ... 6 = Sunday (por ex.)
    date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_holiday: bool = False

    role: Optional[Role] = None
    work_shifts: list[WorkShift] = field(default_factory=list)

    def add_shift(self, shift: WorkShift) -> None:
        self.work_shifts.append(shift)
        shift.work_day = self
        shift.work_day_id = self.id
