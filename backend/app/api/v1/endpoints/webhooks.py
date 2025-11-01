import json
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from stripe import Event

from app.core.config import settings
from app.db.session import get_db
from app.services.stripe_service import StripeService
from app.repositories.transaccion_repository import TransaccionRepository

router = APIRouter()
transaccion_repo = TransaccionRepository()


@router.post("/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe signature header")

    # Get webhook secret from environment/config
    endpoint_secret = settings.stripe_webhook_secret

    try:
        # Verify webhook signature
        event = StripeService.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    await handle_stripe_event(event, db)

    return {"status": "success"}


async def handle_stripe_event(event: Event, db: AsyncSession):
    """Handle different Stripe event types."""
    event_type = event['type']
    event_data = event['data']['object']

    if event_type == 'payment_intent.succeeded':
        await handle_payment_succeeded(event_data, db)
    elif event_type == 'payment_intent.payment_failed':
        await handle_payment_failed(event_data, db)
    # Add more event types as needed


async def handle_payment_succeeded(payment_intent: dict, db: AsyncSession):
    """Handle successful payment."""
    payment_intent_id = payment_intent['id']

    # Update transaction status in database
    transaction = await transaccion_repo.update_transaction_status(
        db, payment_intent_id, "succeeded", payment_intent_id
    )

    if not transaction:
        # Log error - transaction not found
        pass


async def handle_payment_failed(payment_intent: dict, db: AsyncSession):
    """Handle failed payment."""
    payment_intent_id = payment_intent['id']

    # Update transaction status in database
    transaction = await transaccion_repo.update_transaction_status(
        db, payment_intent_id, "failed", payment_intent_id
    )

    if not transaction:
        # Log error - transaction not found
        pass