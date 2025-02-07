from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routers import router as all_routers
from config import settings
from middleware import AuthMiddleware
# Инициализация FastAPI
app = FastAPI()

app.add_middleware(AuthMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session",
    same_site="lax",  # Защита от CSRF
    https_only=False,  # Включить True для продакшена
    max_age=86400  # Время жизни cookie (24 часа)
)


app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(all_routers)
