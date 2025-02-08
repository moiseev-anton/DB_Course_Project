from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import UOWDep, ScooterServiceDep, RentalServiceDep, UserAuthDep, RentalForm
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/create/{scooter_id}", name="create_rental", response_class=HTMLResponse)
async def create_rental(
        request: Request,
        scooter_id: int,
        scooter_service: ScooterServiceDep,
        uow: UOWDep,
        user: UserAuthDep
):
    scooter = await scooter_service.get_available_scooter(uow, scooter_id)
    tariff = scooter.tariff
    unit_minutes = int(tariff.unit.total_seconds() // 60)

    return templates.TemplateResponse(
        "/rent/start.html",
        {
            "request": request,
            "scooter": scooter,
            "tariff": tariff,
            "unit_minutes": unit_minutes,
            "max_units": 24 * 60 // unit_minutes  # Макс 24 часа
        }
    )


@router.post("/create/{scooter_id}", name="create_rental")
async def create_rental(
        scooter_id: int,
        form_data: RentalForm,
        rental_service: RentalServiceDep,
        uow: UOWDep,
        user: UserAuthDep
):
    async with uow:
        try:
            # Получаем самокат с тарифом
            rental_id = await rental_service.create_rental(uow, user.id, scooter_id, form_data)

            return RedirectResponse(f"/", status_code=303)

        except Exception as e:
            await uow.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/current_rental/", name="current_rental", response_class=HTMLResponse)
async def current_rental(
        request: Request,
        rental_service: RentalServiceDep,
        uow: UOWDep,
        user: UserAuthDep
):
    rental = await rental_service.get_current_rental(uow, user.id)
    if rental:
        return templates.TemplateResponse(
            "rent/current.html",
            {
                "request": request,
                "rental": rental,
                "user": user
            }
        )
    return RedirectResponse(url="/scooters", status_code=303)


@router.post("/{rental_id}/pay", name="pay_rent", response_class=HTMLResponse)
async def payment(
        rental_id: int,
        request: Request,
        rental_service: RentalServiceDep,
        uow: UOWDep,
        user: UserAuthDep,
):
    await rental_service.pay_rent(uow, rental_id)
    return RedirectResponse(url="/", status_code=303)


@router.post("/{rental_id}/cancel", name="cancel_rent", response_class=HTMLResponse)
async def cancel(
        rental_id: int,
        request: Request,
        rental_service: RentalServiceDep,
        uow: UOWDep,
        user: UserAuthDep,
):
    await rental_service.cancel_rent(uow, rental_id)
    return RedirectResponse(url="/", status_code=303)
