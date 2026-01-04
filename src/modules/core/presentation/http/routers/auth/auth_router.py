# app/presentation/api/routes_auth.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from src.core.config.config import get_settings
from src.modules.core.application.usecases.auth.auth_service import AuthService
from src.modules.core.application.usecases.auth.utils import InvalidCredentials, RefreshExpired, RefreshInvalid, RefreshNotFound, RefreshReuseDetected
from src.modules.core.presentation.http.dependencies.auth_dependencies import get_auth_service
from src.modules.core.presentation.http.routers.auth.cookies import set_access_cookie, set_refresh_cookie
from src.modules.core.presentation.http.schemas.pydantic.auth_schema import LoginRequestBody

router = APIRouter(prefix="/auth", tags=["auth"])

settings = get_settings()


@router.post("/login")
async def login(response: Response, body: LoginRequestBody, auth_service: AuthService = Depends(get_auth_service)):
    try:
        result = await auth_service.login(body.email, body.password)
    except InvalidCredentials as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas") from exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    # coloca access + refresh em cookies HttpOnly
    set_access_cookie(response, result["access_token"])
    set_refresh_cookie(response, result["refresh_jti"], result["refresh_token"])

    # opcional: retornar user_id ou outros dados minimalistas
    return {"user_id": result["user_id"]}


@router.post("/refresh")
async def refresh(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    cookie = request.cookies.get(settings.REFRESH_COOKIE_NAME)

    if not cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token ausente")

    # parse cookie (formato jti:raw)
    try:
        jti, raw = cookie.split(":", 1)
    except ValueError as exc:
        # cookie malformado
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh cookie malformado") from exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor") from e

    try:
        new = await auth_service.rotate_refresh(raw, jti)
    except (RefreshNotFound, RefreshExpired, RefreshReuseDetected, RefreshInvalid) as e:
        # no caso de reutilização ou invalidação, limpamos cookie
        response.delete_cookie(settings.REFRESH_COOKIE_NAME, path="/")
        response.delete_cookie(settings.ACCESS_COOKIE_NAME, path="/")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    # sobrescreve cookies com novos tokens
    set_access_cookie(response, new["access_token"])
    set_refresh_cookie(response, new["refresh_jti"], new["refresh_token"])

    return {"user_id": new["user_id"]}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    cookie = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if cookie:
        try:
            jti, raw = cookie.split(":", 1)
        except ValueError:
            jti, raw = None, None
        except Exception:
            jti, raw = None, None

        if jti and raw:
            await auth_service.logout_by_cookie(raw, jti)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    # sempre limpa cookies do cliente
    response.delete_cookie(settings.REFRESH_COOKIE_NAME, path="/")
    response.delete_cookie(settings.ACCESS_COOKIE_NAME, path="/")

    return response


@router.get("/me")
async def return_user_by_access_token(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    access = request.cookies.get(settings.ACCESS_COOKIE_NAME)

    try:
        if not access:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access not provided")

        user = await auth_service.return_user_by_access_token(access)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not find user for provided access token")

        return user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is not valid") from e
