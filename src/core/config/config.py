# config.py
import os
from functools import lru_cache
from typing import Literal

# from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-super-secret")

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    # nomes de cookie
    ACCESS_COOKIE_NAME: str = "access_token"

    REFRESH_COOKIE_NAME: str = "refresh_token"

    # cookie policy (em produção ajuste secure=True e domain)
    COOKIE_SECURE: bool = False  # True em produção (HTTPS)

    COOKIE_SAMESITE: Literal["lax", "strict", "none"] | None = "lax"  # 'Lax' ou 'Strict' dependendo do fluxo

    COOKIE_HTTPONLY: bool = True

    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///./test.db")

    SERVER_URL: str = os.getenv("SERVER_URL", "http://localhost:8005/api")

    ACCESS_SECRET: str = os.getenv("ACCESS_SECRET", "change-me-super-secret")

    # email (SMTP)
    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_USE_SSL: bool = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "")
    EMAIL_TIMEOUT: int = int(os.getenv("EMAIL_TIMEOUT", "10"))

    # email (Mailjet)
    MAILJET_API_KEY: str = os.getenv("MAILJET_API_KEY", os.getenv("MJ_APIKEY_PUBLIC", ""))
    MAILJET_SECRET_KEY: str = os.getenv("MAILJET_SECRET_KEY", os.getenv("MJ_APIKEY_PRIVATE", ""))

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
