from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, update

from app.models.ticket import Ticket
from app.repositories.base import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self):
        super().__init__(Ticket)

    async def get_available_tickets(self, db: AsyncSession, rifa_id: str, limit: Optional[int] = None) -> List[Ticket]:
        query = select(Ticket).where(
            and_(Ticket.rifa_id == rifa_id, Ticket.estado == "disponible")
        ).order_by(Ticket.numero)

        if limit:
            query = query.limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def get_available_tickets_with_lock(self, db: AsyncSession, rifa_id: str, limit: Optional[int] = None) -> List[Ticket]:
        query = select(Ticket).where(
            and_(Ticket.rifa_id == rifa_id, Ticket.estado == "disponible")
        ).order_by(Ticket.numero).with_for_update()

        if limit:
            query = query.limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def get_tickets_by_user(self, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Ticket]:
        query = select(Ticket).where(Ticket.usuario_id == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_tickets_by_rifa(self, db: AsyncSession, rifa_id: str) -> List[Ticket]:
        query = select(Ticket).where(Ticket.rifa_id == rifa_id).order_by(Ticket.numero)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_next_ticket_number(self, db: AsyncSession, rifa_id: str) -> int:
        query = select(Ticket).where(Ticket.rifa_id == rifa_id).order_by(desc(Ticket.numero)).limit(1)
        result = await db.execute(query)
        last_ticket = result.scalar_one_or_none()
        return (last_ticket.numero + 1) if last_ticket else 1

    async def update_ticket_status(self, db: AsyncSession, ticket_id: str, status: str, user_id: str = None, transaction_id: str = None) -> Optional[Ticket]:
        ticket = await self.get_by_id(db, ticket_id)
        if ticket:
            ticket.estado = status
            if user_id:
                ticket.usuario_id = user_id
            if transaction_id:
                ticket.transaccion_id = transaction_id
            await db.commit()
            await db.refresh(ticket)
        return ticket

    async def bulk_update_tickets(self, db: AsyncSession, ticket_ids: List[str], updates: dict) -> None:
        query = update(Ticket).where(Ticket.id.in_(ticket_ids)).values(updates)
        await db.execute(query)
        await db.commit()