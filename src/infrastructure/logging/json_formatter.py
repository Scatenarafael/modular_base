from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from src.core.logging.context import get_request_id, get_user_id


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_request_id(),
            "user_id": get_user_id(),
        }

        # Campos extras (quando você usa logger.info("...", extra={...})
        extras = getattr(record, "fields", None)
        if isinstance(extras, dict):
            base.update(extras)

        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(base, ensure_ascii=False)
