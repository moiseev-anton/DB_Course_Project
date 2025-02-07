from fastapi import APIRouter

router = APIRouter()

# Тут будем подключать эндпоинты. Например:
# router.include_router(users.router, prefix="/users", tags=["Users"])
# router.include_router(scooters.router, prefix="/scooters", tags=["Scooters"])