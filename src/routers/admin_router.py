from datetime import date

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dependencies import (
    UOWDep,
    ScooterServiceDep,
    RentalServiceDep,
    AdminAuthDep,
)
from schemas import DateRange

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(
    request: Request,
    admin: AdminAuthDep,
    scooter_service: ScooterServiceDep,
    rental_service: RentalServiceDep,
    uow: UOWDep,
    start_date: date = Query(default_factory=lambda: DateRange.default().start_date),
    end_date: date = Query(default_factory=lambda: DateRange.default().end_date),
):
    date_range = DateRange(start_date=start_date, end_date=end_date)

    rental_report = await rental_service.get_stats(uow, date_range)
    financial_report = await rental_service.get_financial_report(uow, date_range)
    scooter_usage = await scooter_service.get_usage_stats(uow, date_range)

    return templates.TemplateResponse(
        "admin/analytics.html",
        {
            "request": request,
            "user": admin,
            "rental_report": rental_report,
            "scooter_usage": scooter_usage,
            "financial_report": financial_report,
            "date_range": date_range,
            "today": date.today(),
        },
    )
