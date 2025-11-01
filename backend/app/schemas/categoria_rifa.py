from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from uuid import UUID


class CategoriaRifaBase(BaseModel):
    nombre: str
    color: Optional[str] = None
    valor_boleta: int
    total_recaudo: Optional[int] = None
    rake: Optional[Decimal] = None
    fondo_premios: Optional[int] = None
    premio_por_ganador: Optional[int] = None
    comentario: Optional[str] = None


class CategoriaRifaCreate(CategoriaRifaBase):
    pass


class CategoriaRifaUpdate(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None
    valor_boleta: Optional[int] = None
    total_recaudo: Optional[int] = None
    rake: Optional[Decimal] = None
    fondo_premios: Optional[int] = None
    premio_por_ganador: Optional[int] = None
    comentario: Optional[str] = None


class CategoriaRifaOut(CategoriaRifaBase):
    id: UUID

    class Config:
        from_attributes = True