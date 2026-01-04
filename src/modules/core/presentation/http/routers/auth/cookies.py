from fastapi import Response

from src.core.config.config import get_settings

settings = get_settings()


def set_access_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key=settings.ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )


def set_refresh_cookie(response: Response, jti: str, raw_refresh: str) -> None:
    # expected cookie format: "<jti>:<raw_refresh>"
    cookie_value = f"{jti}:{raw_refresh}"
    max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=cookie_value,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=max_age,
        path="/",
    )
