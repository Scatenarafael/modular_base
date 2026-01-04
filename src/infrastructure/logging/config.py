from __future__ import annotations

from logging.config import dictConfig

from src.infrastructure.logging.json_formatter import JsonFormatter


def configure_logging(level: str = "INFO") -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
            },
            "root": {
                "level": level,
                "handlers": ["console"],
            },
            # Ajustes úteis:
            "loggers": {
                "uvicorn.error": {"level": level},
                "uvicorn.access": {"level": "WARNING"},  # access log pode duplicar seu middleware
                "sqlalchemy.engine": {"level": "WARNING"},
            },
        }
    )
