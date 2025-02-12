from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


from services import UserService
from unitofwork import UnitOfWork


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Пропускаем middleware для публичных роутов
        if request.url.path in ["/login", "/register", "/logout"]:
            return await call_next(request)

        user = None
        # Получаем user_id из сессии
        user_id = request.session.get("user_id")
        if user_id:
            uow = UnitOfWork()
            user = await UserService().get_user_by_id(user_id=user_id, uow=uow)

        # Добавляем данные пользователя в request.state
        request.state.user = user

        # Продолжаем обработку запроса
        response = await call_next(request)
        return response
