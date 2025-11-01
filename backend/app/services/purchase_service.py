import stripe
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from datetime import datetime
from uuid import uuid4

from app.core.config import settings
from app.models.ticket import Ticket
from app.models.transaccion import Transaccion
from app.models.rifa import Rifa
from app.repositories.ticket_repository import TicketRepository
from app.repositories.rifa_repository import RifaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.schemas.ticket import TicketPurchase, TicketPurchaseResponse


class PurchaseService:
    def __init__(self):
        self.ticket_repo = TicketRepository()
        self.rifa_repo = RifaRepository()
        self.transaccion_repo = TransaccionRepository()
        stripe.api_key = settings.stripe_secret_key

    async def purchase_tickets(self, db: AsyncSession, purchase: TicketPurchase, user_id: str) -> TicketPurchaseResponse:
        transaction = None
        try:
            # Check idempotency
            existing_transaction = await self.transaccion_repo.get_by_idempotency_key(db, purchase.idempotency_key)
            if existing_transaction:
                # Return existing purchase result
                tickets = await self.ticket_repo.get_tickets_by_user(db, user_id)
                return TicketPurchaseResponse(tickets=tickets, transaccion_id=existing_transaction.id)

            # Verify rifa is active
            rifa = await self.rifa_repo.get_active_rifa(db, str(purchase.rifa_id))
            if not rifa:
                raise ValueError("Rifa not found or not active")

            # Start database transaction
            async with db.begin():

                # Check available tickets with lock
                available_tickets = await self.ticket_repo.get_available_tickets_with_lock(db, str(purchase.rifa_id), purchase.quantity)
                if len(available_tickets) < purchase.quantity:
                    raise ValueError("Not enough tickets available")

                # Calculate total amount (assuming fixed price per ticket)
                ticket_price = 1000  # COP
                total_amount = len(available_tickets) * ticket_price

                # Process payment with Stripe (sandbox mode)
                payment_intent = stripe.PaymentIntent.create(
                    amount=total_amount,
                    currency="cop",
                    metadata={
                        "rifa_id": str(purchase.rifa_id),
                        "user_id": user_id,
                        "quantity": purchase.quantity,
                        "idempotency_key": purchase.idempotency_key
                    }
                )

                # Create transaction record
                transaction = Transaccion(
                    user_id=user_id,
                    amount=total_amount,
                    currency="COP",
                    provider="stripe",
                    provider_ref=payment_intent.id,
                    idempotency_key=purchase.idempotency_key,
                    status="pending"
                )
                db.add(transaction)
                await db.flush()  # Get transaction ID without committing

                # Update tickets
                ticket_ids = [str(ticket.id) for ticket in available_tickets]
                now = datetime.utcnow()

                await self.ticket_repo.bulk_update_tickets(db, ticket_ids, {
                    "usuario_id": user_id,
                    "estado": "vendido",
                    "comprado_en": now,
                    "transaccion_id": str(transaction.id)
                })

                # Confirm payment
                stripe.PaymentIntent.confirm(payment_intent.id)

                # Update transaction status
                transaction.status = "succeeded"
                await db.commit()

            # Refresh tickets
            updated_tickets = await self.ticket_repo.get_tickets_by_user(db, user_id, limit=purchase.quantity)

            return TicketPurchaseResponse(
                tickets=updated_tickets,
                transaccion_id=transaction.id
            )

        except stripe.error.StripeError as e:
            # Update transaction status to failed
            if transaction:
                transaction.status = "failed"
                await db.commit()
            raise ValueError(f"Payment failed: {str(e)}")
        except Exception as e:
            if transaction:
                transaction.status = "failed"
                await db.commit()
            raise ValueError(f"Purchase failed: {str(e)}")