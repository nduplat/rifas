from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.transaccion import Transaccion
from app.repositories.base import BaseRepository


class TransaccionRepository(BaseRepository[Transaccion]):
    def __init__(self):
        super().__init__(Transaccion)

    async def get_by_idempotency_key(self, db: AsyncSession, idempotency_key: str) -> Optional[Transaccion]:
        query = select(Transaccion).where(Transaccion.idempotency_key == idempotency_key)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_transactions(self, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Transaccion]:
        query = select(Transaccion).where(Transaccion.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def update_transaction_status(self, db: AsyncSession, provider_ref: str, status: str, transaction_id: Optional[str] = None) -> Optional[Transaccion]:
        # Find transaction by provider_ref (Stripe payment_intent_id)
        query = select(Transaccion).where(Transaccion.provider_ref == provider_ref)
        result = await db.execute(query)
        transaction = result.scalar_one_or_none()

        if transaction:
            transaction.status = status
            await db.commit()
            await db.refresh(transaction)
        return transaction