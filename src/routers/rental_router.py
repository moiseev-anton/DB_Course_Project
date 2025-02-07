from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import UOWDep, ScooterServiceDep, RentalServiceDep, UserAuthDep, RentalForm
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/rent")
templates = Jinja2Templates(directory="templates")


@router.get("/{scooter_id}", name="rent_scooter", response_class=HTMLResponse)
async def rent_scooter_page(
        request: Request,
        scooter_id: int,
        scooter_service: ScooterServiceDep,
        uow: UOWDep,
        user: UserAuthDep
):
    scooter = await scooter_service.get_available_scooter(uow, scooter_id)

    return templates.TemplateResponse(
        "rent/start.html",
        {
            "request": request,
            "scooter": scooter,
            "user": user
        }
    )


@router.post("/{scooter_id}", name="start_rental")
async def start_rental(
        request: Request,
        rental_data: RentalForm,
        rental_service: RentalServiceDep,
        uow: UOWDep,
        user: UserAuthDep
):
    try:
        # Создаем аренду
        await rental_service.create_rental(uow, rental_data)
        return RedirectResponse(
            url=router.url_path_for("current_rental"),
            status_code=303
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{rental_id}", name="current_rental", response_class=HTMLResponse)
async def rent_scooter_page(
        request: Request,
        scooter_id: int,
        scooter_service: ScooterServiceDep,
        uow: UOWDep,
        user: UserAuthDep
):
    scooter = await scooter_service.get_available_scooter(uow, scooter_id)

    return templates.TemplateResponse(
        "rent/start.html",
        {
            "request": request,
            "scooter": scooter,
            "user": user
        }
    )