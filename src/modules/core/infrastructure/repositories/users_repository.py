from typing import Optional, Sequence

from passlib.context import CryptContext
from sqlalchemy import delete, orm, select

from src.infrastructure.database.settings.connection import DbConnectionHandler
from src.modules.core.domain.entities.user import User
from src.modules.core.domain.interfaces.iusers_repository import IUsersRepository
from src.modules.core.infrastructure.mappers.user_mapper import UserMapper
from src.modules.core.infrastructure.models.company_model import CompanyModel
from src.modules.core.infrastructure.models.role_model import RoleModel
from src.modules.core.infrastructure.models.user_company_role_model import UserCompanyRoleModel
from src.modules.core.infrastructure.models.user_model import UserModel

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersRepository(IUsersRepository):
    @classmethod
    async def list(cls) -> Optional[list[User]]:
        async with DbConnectionHandler() as database:
            try:
                if database.session:
                    result = await database.session.execute(select(UserModel).order_by(UserModel.created_at.desc()))

                    user_models: Sequence[UserModel] = result.scalars().all()

                    for user in user_models:
                        delattr(user, "hashed_password")

                    users = [UserMapper.to_entity(user) for user in user_models]

                    return users
            except Exception as exception:
                raise exception

    @classmethod
    async def create(cls, user: User) -> Optional[User]:
        async with DbConnectionHandler() as database:
            try:
                new_register = UserModel(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    hashed_password=pwd_ctx.hash(user.password),
                    active=user.active,
                )

                if not new_register:
                    raise ValueError("Could not create user")

                if database.session:
                    database.session.add(new_register)

                    await database.session.commit()

                    await database.session.refresh(new_register)

                    delattr(new_register, "hashed_password")

                    user = UserMapper.to_entity(new_register)

                    return user
            except Exception as exception:
                raise exception

    @classmethod
    async def get_by_id(cls, id: str) -> Optional[User]:
        async with DbConnectionHandler() as database:  # type: ignore
            try:
                if not database.session:
                    return None

                stmt = (
                    select(UserModel)
                    .where(UserModel.id == id)
                    .options(
                        # 1) Carrega apenas is_owner em UserCompanyRole
                        #    + company.id / company.name
                        orm.selectinload(UserModel.companies_roles)
                        .load_only(UserCompanyRoleModel.is_owner)  # type: ignore
                        .selectinload(UserCompanyRoleModel.company)
                        .load_only(CompanyModel.id, CompanyModel.name),  # type: ignore
                        # 2) Carrega o role com apenas id / name
                        orm.selectinload(UserModel.companies_roles).selectinload(UserCompanyRoleModel.role).load_only(RoleModel.id, RoleModel.name),
                    )
                )

                result = await database.session.execute(stmt)

                user_model: UserModel | None = result.scalars().unique().first()

                if not user_model:
                    raise LookupError("User not found!")

                user = UserMapper.to_entity(user_model)

                return user

            except Exception:
                if database.session:
                    await database.session.rollback()
                raise

    @classmethod
    async def get_by_email(cls, email: str) -> Optional[User]:
        async with DbConnectionHandler() as database:
            try:
                if database.session:
                    result = await database.session.execute(select(User).where(User.email == email))  # type: ignore
                    user = result.scalars().first()
                    if not user:
                        raise LookupError("User not found!")
                    return user
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception

    @classmethod
    async def partial_update_by_id(cls, id: str, first_name: str | None, last_name: str | None, email: str | None, hashed_password: str | None, active: bool | None) -> Optional[User]:
        async with DbConnectionHandler() as database:
            try:
                if database.session:
                    result = await database.session.execute(select(User).filter(User.id == id))  # type: ignore
                    user = result.scalars().first()
                    if not user:
                        raise ValueError("User not found")

                args = {"first_name": first_name, "last_name": last_name, "email": email, "hashed_password": hashed_password, "active": active}

                not_none_args = {k: v for k, v in args.items() if v is not None}

                for attr, value in not_none_args.items():
                    setattr(user, attr, value)

                if database.session:
                    database.session.add(user)
                    await database.session.commit()
                    await database.session.refresh(user)
                    return user  # type: ignore
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception

    @classmethod
    async def delete(cls, id: str):
        async with DbConnectionHandler() as database:
            try:
                if database.session:
                    await database.session.execute(delete(UserModel).where(UserModel.id == id))
                    await database.session.commit()
            except Exception as exception:
                if database.session:
                    await database.session.rollback()
                raise exception

    @classmethod
    def verify_password(cls, plain: str, hashed: str) -> bool:
        return pwd_ctx.verify(plain, hashed)
