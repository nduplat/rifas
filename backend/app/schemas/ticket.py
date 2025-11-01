from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TicketBase(BaseModel):
    rifa_id: UUID
    numero: int
    precio: Optional[int] = None


class TicketCreate(TicketBase):
    pass


class TicketOut(TicketBase):
    id: UUID
    usuario_id: Optional[UUID] = None
    comprado_en: Optional[datetime] = None
    estado: str
    transaccion_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class TicketPurchase(BaseModel):
    rifa_id: UUID
    user_id: UUID
    quantity: int
    payment_method: str = "stripe"
    idempotency_key: str


class TicketPurchaseResponse(BaseModel):
    tickets: List[TicketOut]
    transaccion_id: UUID