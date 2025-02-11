from fastapi import Request, HTTPException


def auth_required(request: Request):
    """Зависимость для обязательной авторизации"""
    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=307, headers={"Location": f"/login?next={request.url.path}"}
        )
    return user


def admin_required(request: Request):
    user = auth_required(request)
    if user.role != "ADMIN":
        raise HTTPException(status_code=307, headers={"Location": f"/"})
    return user
