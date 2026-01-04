from src.modules.core.application.usecases.users.create_user_usecase import CreateUserUseCase
from src.modules.core.application.usecases.users.delete_user_usecase import DeleteUserUseCase
from src.modules.core.application.usecases.users.list_users_usecase import ListUsersUseCase
from src.modules.core.application.usecases.users.retrieve_user_usecase import RetrieveUserUseCase
from src.modules.core.application.usecases.users.update_user_usecase import UpdateUserUseCase
from src.modules.core.infrastructure.repositories.users_repository import UsersRepository
from src.modules.core.presentation.http.dependencies.email_dependencies import get_send_email_usecase


def get_create_user_usecase() -> CreateUserUseCase:
    return CreateUserUseCase(users_repository=UsersRepository(), send_email_usecase=get_send_email_usecase())


def get_list_users_usecase() -> ListUsersUseCase:
    return ListUsersUseCase(UsersRepository())


def get_retrieve_user_usecase() -> RetrieveUserUseCase:
    return RetrieveUserUseCase(UsersRepository())


def get_update_user_usecase() -> UpdateUserUseCase:
    return UpdateUserUseCase(UsersRepository())


def get_delete_user_usecase() -> DeleteUserUseCase:
    return DeleteUserUseCase(UsersRepository())
