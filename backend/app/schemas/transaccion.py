from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TransaccionBase(BaseModel):
    user_id: UUID
    amount: int
    currency: str = "COP"
    provider: Optional[str] = None
    provider_ref: Optional[str] = None
    status: str = "pending"


class TransaccionCreate(TransaccionBase):
    pass


class TransaccionUpdate(BaseModel):
    status: Optional[str] = None
    provider_ref: Optional[str] = None


class TransaccionOut(TransaccionBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True