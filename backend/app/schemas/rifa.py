from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class RifaBase(BaseModel):
    nombre: str
    categoria_id: UUID
    loteria_id: UUID
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    numero_ganadores: int = 1
    reglas: Dict[str, Any] = {}
    total_boletas: int = 100


class RifaCreate(RifaBase):
    pass


class RifaUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria_id: Optional[UUID] = None
    loteria_id: Optional[UUID] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    numero_ganadores: Optional[int] = None
    estado: Optional[str] = None
    reglas: Optional[Dict[str, Any]] = None
    total_boletas: Optional[int] = None


class RifaOut(RifaBase):
    id: UUID
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True


class RifaList(BaseModel):
    id: UUID
    nombre: str
    categoria_id: UUID
    loteria_id: UUID
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: str
    total_boletas: int
    creado_en: datetime

    class Config:
        from_attributes = True