from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if request.state.user:
        return RedirectResponse(url="/rent/current_rental", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

