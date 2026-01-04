from src.modules.core.application.usecases.auth.auth_service import AuthService
from src.modules.core.infrastructure.repositories.jwt.jwt_repository import JWTRepository
from src.modules.core.infrastructure.repositories.users_repository import UsersRepository


def get_auth_service() -> AuthService:
    return AuthService(UsersRepository(), JWTRepository())
