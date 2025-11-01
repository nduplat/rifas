from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    rol: str = "jugador"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    rol: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(UserBase):
    id: UUID
    creado_en: datetime
    is_active: bool

    class Config:
        from_attributes = True