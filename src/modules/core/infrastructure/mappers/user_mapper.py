# src/infrastructure/database/mappers/company_mapper.py
from uuid import UUID

from src.modules.core.domain.entities.User import User
from src.modules.core.infrastructure.models.user_model import UserModel


class UserMapper:
    @staticmethod
    def to_entity(model: UserModel) -> User:
        return User(
            id=UUID(str(model.id)),
            first_name=str(model.first_name),
            last_name=str(model.last_name),
            email=str(model.email),
            hashed_password=str(model.hashed_password),
            active=bool(model.active),
        )

    @staticmethod
    def from_entity(entity: User) -> UserModel:
        # para "create" normalmente você NÃO passa id nem created_at,
        # mas deixo explícito aqui só como exemplo
        return UserModel(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            hashed_password=entity.hashed_password,
            active=entity.active,
        )
