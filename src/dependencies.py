from typing import Annotated

from fastapi import Depends

from auth import auth_required, admin_required
from schemas import (
    UserLogin,
    UserRegister,
    UserDisplay,
    UserUpdate,
    PasswordChange,
    RentalCreate,
    DateRange,
)
from services import (
    ScooterService,
    UserService,
    LocationService,
    RentalService,
    # PaymentService,
)
from unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

# Services
UserServiceDep = Annotated[UserService, Depends(UserService)]
ScooterServiceDep = Annotated[ScooterService, Depends(ScooterService)]
LocationServiceDep = Annotated[LocationService, Depends(LocationService)]
RentalServiceDep = Annotated[RentalService, Depends(RentalService)]
# PaymentServiceDep = Annotated[PaymentService, Depends(PaymentService)]

# Forms
LoginForm = Annotated[UserLogin, Depends(UserLogin.as_form)]
RegisterForm = Annotated[UserRegister, Depends(UserRegister.as_form)]
UpdateForm = Annotated[UserUpdate, Depends(UserUpdate.as_form)]
PasswordChangeForm = Annotated[PasswordChange, Depends(PasswordChange.as_form)]
RentalForm = Annotated[RentalCreate, Depends(RentalCreate.as_form)]
DateRangeForm = Annotated[DateRange, Depends(DateRange)]

# Auth
UserAuthDep = Annotated[UserDisplay, Depends(auth_required)]
AdminAuthDep = Annotated[UserDisplay, Depends(admin_required)]
