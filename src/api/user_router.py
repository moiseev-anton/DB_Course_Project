from fastapi import APIRouter

from dependencies import UOWDep
from schemas.user_schemas import UserRegister, UserUpdate, UserDisplay
from services.user_service import UserService
from sqlalchemy.dialects.postgresql import UUID

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

#
# @router.post("")
# async def add_user(
#     user: UserCreate,
#     uow: UOWDep,
# ):
#     user_id = await UsersService().add_user(uow, user)
#     return {"user_id": user_id}
#
#
# @router.get("")
# async def get_users(
#     uow: UOWDep,
# ):
#     users = await UsersService().get_users(uow)
#     return users

