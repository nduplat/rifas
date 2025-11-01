from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class GanadorBase(BaseModel):
    ticket_id: UUID
    monto_ganado: int
    fecha_pago: Optional[datetime] = None
    referencia_pago: Optional[str] = None


class GanadorCreate(GanadorBase):
    pass


class GanadorUpdate(BaseModel):
    monto_ganado: Optional[int] = None
    fecha_pago: Optional[datetime] = None
    referencia_pago: Optional[str] = None


class GanadorOut(GanadorBase):
    id: UUID

    class Config:
        from_attributes = True