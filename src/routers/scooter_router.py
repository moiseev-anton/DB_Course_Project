from typing import Optional

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dependencies import UOWDep, ScooterServiceDep, LocationServiceDep

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/scooters")


@router.get("", name="scooters_list", response_class=HTMLResponse)
async def scooters_list(
    request: Request,
    uow: UOWDep,
    scooter_service: ScooterServiceDep,
    location_service: LocationServiceDep,
    location_id: Optional[int] = Query(None, alias="location_id", ge=0),
    min_battery: Optional[int] = Query(None, ge=0, le=100),
):
    locations = await location_service.get_all_locations(uow)
    scooters = await scooter_service.get_available_scooters(
        uow, location_id, min_battery
    )
    return templates.TemplateResponse(
        "scooters/list.html",
        {
            "request": request,
            "scooters": scooters,
            "locations": locations,
            "user": request.state.user,
            "location_id": location_id,
            "min_battery": min_battery,
        },
    )


@router.get("/{scooter_id}", name="scooter_detail", response_class=HTMLResponse)
async def scooter_detail(
    request: Request,
    scooter_id: int,
    uow: UOWDep,
    scooter_service: ScooterServiceDep,
):
    scooter = await scooter_service.get_available_scooter(uow, scooter_id)
    return templates.TemplateResponse(
        "scooters/detail.html", {"request": request, "scooter": scooter}
    )
