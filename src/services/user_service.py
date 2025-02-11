from typing import List
from uuid import UUID

from passlib.context import CryptContext

from schemas import UserRegister, UserUpdate, UserLogin, UserCreate, UserDisplay, PasswordChange
from unitofwork import IUnitOfWork

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    async def authenticate_user(
            self, uow: IUnitOfWork, creds: UserLogin
    ) -> UserDisplay:
        async with uow:
            user = await uow.users.get_one(phone=creds.phone, is_active=True)
            if not user or not await self.verify_password(
                    creds.password, user.password_hash
            ):
                raise ValueError("Неверный телефон или пароль")
            return UserDisplay.model_validate(user)

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def get_user_by_id(user_id: str, uow: IUnitOfWork) -> UserDisplay:
        async with uow:
            user = await uow.users.get_one(id=UUID(user_id))
            if not user:
                raise ValueError("Пользователь не найден")
            return UserDisplay.model_validate(user)

    @staticmethod
    async def get_all_active_users(uow: IUnitOfWork) -> List[UserDisplay]:
        async with uow:
            users = await uow.users.get_all(is_active=True)
            return list(map(UserDisplay.model_validate, users))

    async def add_user(self, uow: IUnitOfWork, user_data: UserRegister) -> UserDisplay:
        async with uow:
            # Проверяем, существует ли уже пользователь
            existing_user = await uow.users.get_one(phone=user_data.phone)
            if existing_user:
                raise ValueError("Пользователь с таким номером уже зарегистрирован")

            # Хешируем пароль
            hashed_password = self.hash_password(user_data.password)

            new_user = UserCreate(
                **user_data.model_dump(), password_hash=hashed_password
            )
            user = await uow.users.create_one(new_user.model_dump())

            await uow.commit()
            return UserDisplay.model_validate(user)

    @staticmethod
    async def update_user(
            uow: IUnitOfWork, user_id: UUID, user: UserUpdate
    ) -> UserDisplay:
        async with uow:
            existing_user = await uow.users.get_one(phone=user.phone)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Пользователь с таким телефоном уже существует")
            updated_user = await uow.users.update_one(
                id=user_id, data=user.model_dump(exclude_unset=True)
            )
            await uow.commit()  # Подтверждаем изменения
            return UserDisplay.model_validate(updated_user)

    async def change_password(
            self, uow: IUnitOfWork, user_id: UUID, pswd: PasswordChange
    ) -> UserDisplay:
        async with uow:
            user = await uow.users.get_one(id=user_id)
            if not user:
                raise ValueError("Пользователь не найден")

            if not await self.verify_password(pswd.old_password, user.password_hash):
                raise ValueError("Введен неверный пароль")

            password_hash = self.hash_password(pswd.new_password)
            updated_user = await uow.users.update_one(
                id=user_id, data={"password_hash": password_hash}
            )

            await uow.commit()  # Подтверждаем изменения
            return UserDisplay.model_validate(updated_user)
