from src.infrastructure.external_services.email_service.mailjet_email_service import MailjetEmailService
from src.modules.core.application.usecases.users.create_user_usecase import CreateUserUseCase
from src.modules.core.application.usecases.users.delete_user_usecase import DeleteUserUseCase
from src.modules.core.application.usecases.users.list_users_usecase import ListUsersUseCase
from src.modules.core.application.usecases.users.retrieve_user_usecase import RetrieveUserUseCase
from src.modules.core.application.usecases.users.update_user_usecase import UpdateUserUseCase
from src.modules.core.infrastructure.repositories.users_repository import UsersRepository


def get_create_user_usecase():
    return CreateUserUseCase(users_repository=UsersRepository(), email_service=MailjetEmailService(from_email="rafascatena@email.com", from_name="Rafael"))


def get_list_users_usecase():
    return ListUsersUseCase(UsersRepository())


def get_retrieve_user_usecase():
    return RetrieveUserUseCase(UsersRepository())


def get_update_user_usecase():
    return UpdateUserUseCase(UsersRepository())


def get_delete_user_usecase():
    return DeleteUserUseCase(UsersRepository())
