# src/infrastructure/database/mappers/company_mapper.py
from typing import Optional
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
            active=entity.active,
        )


class PayloadUpdateUser:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None
