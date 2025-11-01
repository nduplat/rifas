from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.rifa import Rifa
from app.models.ticket import Ticket
from app.repositories.base import BaseRepository


class RifaRepository(BaseRepository[Rifa]):
    def __init__(self):
        super().__init__(Rifa)

    async def get_active_rifa(self, db: AsyncSession, rifa_id: str) -> Optional[Rifa]:
        query = select(Rifa).where(
            Rifa.id == rifa_id,
            Rifa.estado == "activa"
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_rifa_with_tickets_count(self, db: AsyncSession, rifa_id: str) -> Optional[Rifa]:
        rifa_query = select(Rifa).where(Rifa.id == rifa_id)
        rifa_result = await db.execute(rifa_query)
        rifa = rifa_result.scalar_one_or_none()
        if rifa:
            count_query = select(func.count(Ticket.id)).where(
                Ticket.rifa_id == rifa_id,
                Ticket.estado == "disponible"
            )
            count_result = await db.execute(count_query)
            available_count = count_result.scalar()
            rifa.available_tickets = available_count
        return rifa