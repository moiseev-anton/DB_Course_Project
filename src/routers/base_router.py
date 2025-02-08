from fastapi import APIRouter
from .index_router import router as index_router
from .scooter_router import router as scooter_router
from .auth_router import router as auth_router
from .user_router import router as user_router
from .rental_router import router as rental_router

router = APIRouter()

router.include_router(index_router)
router.include_router(scooter_router, tags=["Scooters"])
router.include_router(auth_router)
router.include_router(user_router, prefix="/user/profile", tags=["User"])
router.include_router(rental_router, prefix="/rent", tags=["Rent"])

