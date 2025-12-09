from fastapi import APIRouter, Depends

from src.modules.core.application.usecases.users.create_user_usecase import CreateUserUseCase
from src.modules.core.application.usecases.users.delete_user_usecase import DeleteUserUseCase
from src.modules.core.application.usecases.users.list_users_usecase import ListUsersUseCase
from src.modules.core.application.usecases.users.retrieve_user_usecase import RetrieveUserUseCase
from src.modules.core.application.usecases.users.update_user_usecase import UpdateUserUseCase
from src.modules.core.presentation.http.routers.users.utils import get_create_user_usecase, get_delete_user_usecase, get_list_users_usecase, get_retrieve_user_usecase, get_update_user_usecase
from src.modules.core.presentation.http.schemas.dtos.users_dto import CreateUserPayloadDTO, UpdateUserPayloadDTO
from src.modules.core.presentation.http.schemas.pydantic.user_schema import PayloadUpdateUser, UserRequestBody

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/register")
async def create(payload: UserRequestBody, create_usecase: CreateUserUseCase = Depends(get_create_user_usecase)):
    new_user = await create_usecase.execute(payload=CreateUserPayloadDTO().to_usecase(payload))
    return new_user


@router.get("")
async def list(list_users_usecase: ListUsersUseCase = Depends(get_list_users_usecase)):
    users = await list_users_usecase.execute()
    return users


@router.get("/{user_id}")
async def retrieve(user_id: str, retrieve_user_usecase: RetrieveUserUseCase = Depends(get_retrieve_user_usecase)):
    user = await retrieve_user_usecase.execute(user_id)
    return user


@router.patch("/{user_id}")
async def update(user_id: str, payload: PayloadUpdateUser, update_usecase: UpdateUserUseCase = Depends(get_update_user_usecase)):
    updated_user = await update_usecase.execute(user_id, payload=UpdateUserPayloadDTO().to_usecase(payload))
    return updated_user


@router.delete("/{user_id}")
async def delete(user_id: str, delete_usecase: DeleteUserUseCase = Depends(get_delete_user_usecase)):
    await delete_usecase.execute(user_id)
    return {"message": "User deleted successfully"}
