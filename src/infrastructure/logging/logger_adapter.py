from __future__ import annotations

import logging
from typing import Any

from src.core.logging.ports import LoggerPort


class LoggerAdapter(LoggerPort):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def debug(self, msg: str, **fields: Any) -> None:
        self._logger.debug(msg, extra={"fields": fields})

    def info(self, msg: str, **fields: Any) -> None:
        self._logger.info(msg, extra={"fields": fields})

    def warning(self, msg: str, **fields: Any) -> None:
        self._logger.warning(msg, extra={"fields": fields})

    def error(self, msg: str, **fields: Any) -> None:
        self._logger.error(msg, extra={"fields": fields})

    def exception(self, msg: str, **fields: Any) -> None:
        self._logger.exception(msg, extra={"fields": fields})
