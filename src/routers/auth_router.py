from fastapi import APIRouter, Depends, Form, Request
from dependencies import UOWDep, UserServiceDep, LoginForm, RegisterForm
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/login")
async def login(
    request: Request, credentials: LoginForm, user_service: UserServiceDep, uow: UOWDep
):
    # Ваш код для аутентификации
    try:
        user = await user_service.authenticate_user(uow, credentials)
        # Сохраняем пользователя в сессию
        request.session["user_id"] = str(user.id)
        request.session["role"] = user.role
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    except ValueError as e:
        return templates.TemplateResponse(
            "/login.html",
            {"request": request, "error": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()  # Очищаем сессию
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    credentials: RegisterForm,
    user_service: UserServiceDep,
    uow: UOWDep,
):
    try:
        new_user = await user_service.add_user(uow, credentials)

        # Записываем пользователя в сессию
        request.session["user_id"] = str(new_user.id)
        request.session["role"] = new_user.role

        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    except ValueError as e:
        return {"error": str(e)}
