from pydantic import BaseModel, field_validator
import re
from typing import Optional
from fastapi import Form
from uuid import UUID


class UserLogin(BaseModel):
    phone: str
    password: str

    @classmethod
    def as_form(cls, phone: str = Form(...), password: str = Form(...)) -> "UserLogin":
        return cls(phone=phone, password=password)


class UserRegister(BaseModel):
    name: str
    surname: Optional[str] = None
    phone: str
    password: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        surname: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
    ) -> "UserRegister":
        return cls(name=name, surname=surname, phone=phone, password=password)


class UserCreate(BaseModel):
    name: str
    surname: Optional[str] = None
    phone: str
    password_hash: str


class UserUpdate(BaseModel):
    name: str
    surname: str
    phone: str

    @classmethod
    def as_form(
        cls, name: str = Form(...), surname: str = Form(...), phone: str = Form(...)
    ) -> "UserUpdate":
        return cls(name=name, surname=surname, phone=phone)

    @field_validator("phone")
    def validate_phone(cls, v):
        if not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Некорректный формат телефона")
        return v


class UserDisplay(BaseModel):
    id: UUID
    name: str
    surname: str
    phone: str
    role: str
    phone: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values.data and v != values.data["new_password"]:
            raise ValueError("Пароли не совпадают")
        return v

    @classmethod
    def as_form(
        cls,
        old_password: str = Form(...),
        new_password: str = Form(...),
        confirm_password: str = Form(...),
    ) -> "PasswordChange":
        return cls(
            old_password=old_password,
            new_password=new_password,
            confirm_password=confirm_password,
        )
