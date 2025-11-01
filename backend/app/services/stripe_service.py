import stripe
from typing import Dict, Any
from app.core.config import settings

stripe.api_key = settings.stripe_secret_key


class StripeService:
    @staticmethod
    def create_payment_intent(amount: int, currency: str = "cop", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a Stripe PaymentIntent for the given amount."""
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata=metadata or {}
        )
        return {
            "id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "amount": payment_intent.amount,
            "currency": payment_intent.currency,
            "status": payment_intent.status
        }

    @staticmethod
    def confirm_payment_intent(payment_intent_id: str) -> Dict[str, Any]:
        """Confirm a PaymentIntent."""
        payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
        return {
            "id": payment_intent.id,
            "status": payment_intent.status,
            "amount": payment_intent.amount,
            "currency": payment_intent.currency
        }

    @staticmethod
    def construct_event(payload: bytes, sig_header: str, endpoint_secret: str) -> stripe.Event:
        """Construct a Stripe Event from webhook payload with signature verification."""
        return stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)