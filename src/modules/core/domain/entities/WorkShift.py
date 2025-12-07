from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.modules.core.domain.entities.WorkDay import WorkDay


@dataclass
class WorkShift:
    id: Optional[int] = None
    # no domínio faz mais sentido ser int, alinhado ao WorkDay.id
    work_day_id: Optional[int] = None
    weekday: Optional[int] = None
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    work_day: Optional[WorkDay] = None
