from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dependencies import UserAuthDep, UOWDep, UserServiceDep, UpdateForm, PasswordChangeForm

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("", name='profile', response_class=HTMLResponse)
async def profile_page(
    request: Request,
    user: UserAuthDep,
):
    return templates.TemplateResponse("user/profile/view.html", {"request": request, "user": user})


@router.get("/edit", name='edit_profile', response_class=HTMLResponse)
async def edit_profile_page(request: Request, user: UserAuthDep):
    return templates.TemplateResponse("user/profile/edit.html", {"request": request, "user": user, "errors": {}})


@router.post("/edit", name='update_profile')
async def update_profile(
    request: Request,
    user: UserAuthDep,
    form_data: UpdateForm,
    uow: UOWDep,
    user_service: UserServiceDep
):

    try:
        user = await user_service.update_user(uow, user.id, form_data)
        return RedirectResponse("/?success=1", status_code=303)
    except Exception as e:
        errors = e.errors() if hasattr(e, 'errors') else [{'msg': str(e)}]
        return templates.TemplateResponse(
            "user/profile/edit.html",
            {
                "request": request,
                "user": user,
                "errors": {error.get('loc', ['unknown'])[0]: error.get('msg', 'Unknown error') for error in errors}
            },
            status_code=400
        )


@router.get("/change-password", name='change_password', response_class=HTMLResponse)
async def change_password_page(request: Request, user: UserAuthDep):
    return templates.TemplateResponse(
        "user/profile/change_password.html",
        {
            "request": request,
            "user": user,
            "errors": {}
        }
    )


@router.post("/change-password", name='update_password',)
async def change_password(
    request: Request,
    form_data: PasswordChangeForm,
    user: UserAuthDep,
    uow: UOWDep,
    user_service: UserServiceDep
):
    try:
        user = await user_service.change_password(uow, user.id, form_data)
        return RedirectResponse("?password_changed=1", status_code=303)
    except Exception as e:
        errors = e.errors() if hasattr(e, 'errors') else [{'msg': str(e)}]
        return templates.TemplateResponse(
            "user/profile/change_password.html",
            {
                "request": request,
                "errors": {error.get('loc', ['unknown'])[0]: error.get('msg', 'Unknown error') for error in errors}
            },
            status_code=400
        )