from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID


class LoteriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    frecuencia: Optional[str] = None
    url_resultados: Optional[str] = None
    meta: Dict[str, Any] = {}


class LoteriaCreate(LoteriaBase):
    pass


class LoteriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    frecuencia: Optional[str] = None
    url_resultados: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class LoteriaOut(LoteriaBase):
    id: UUID

    class Config:
        from_attributes = True