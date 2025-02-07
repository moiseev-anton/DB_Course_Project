from typing import Annotated

from fastapi import Depends

from auth import auth_required
from schemas import (
    UserLogin,
    UserRegister,
    UserDisplay,
    UserUpdate,
    PasswordChange,
    RentalCreate
)
from services import (ScooterService,
                      UserService,
                      LocationService,
                      RentalService
                      )
from unitofwork import IUnitOfWork, UnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

# Services
UserServiceDep = Annotated[UserService, Depends(UserService)]
ScooterServiceDep = Annotated[ScooterService, Depends(ScooterService)]
LocationServiceDep = Annotated[LocationService, Depends(LocationService)]
RentalServiceDep = Annotated[RentalService, Depends(RentalService)]

# Forms
LoginForm = Annotated[UserLogin, Depends(UserLogin.as_form)]
RegisterForm = Annotated[UserRegister, Depends(UserRegister.as_form)]
UpdateForm = Annotated[UserUpdate, Depends(UserUpdate.as_form)]
PasswordChangeForm = Annotated[PasswordChange, Depends(PasswordChange.as_form)]
RentalForm = Annotated[RentalCreate, Depends(RentalCreate.as_form)]

# Auth
UserAuthDep = Annotated[UserDisplay, Depends(auth_required)]
