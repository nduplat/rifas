import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.services.purchase_service import PurchaseService
from app.schemas.ticket import TicketPurchase


class TestPurchaseService:
    def test_purchase_tickets_success(self, db_session, test_user, test_rifa, test_tickets):
        """Test successful ticket purchase."""
        service = PurchaseService()

        purchase = TicketPurchase(
            rifa_id=str(test_rifa.id),
            quantity=2,
            user_id=str(test_user.id),
            idempotency_key="test-key-123"
        )

        with patch('stripe.PaymentIntent.create') as mock_stripe_create, \
             patch('stripe.PaymentIntent.confirm') as mock_stripe_confirm:

            mock_payment_intent = Mock()
            mock_payment_intent.id = "pi_test_123"
            mock_stripe_create.return_value = mock_payment_intent

            result = service.purchase_tickets(db_session, purchase, str(test_user.id))

            assert result.transaccion_id is not None
            assert len(result.tickets) == 2

            # Verify tickets are marked as sold
            for ticket in result.tickets:
                assert ticket.estado == "vendido"
                assert ticket.usuario_id == str(test_user.id)

    def test_purchase_tickets_insufficient_tickets(self, db_session, test_user, test_rifa):
        """Test purchase when not enough tickets available."""
        service = PurchaseService()

        purchase = TicketPurchase(
            rifa_id=str(test_rifa.id),
            quantity=100,  # More than available
            user_id=str(test_user.id),
            idempotency_key="test-key-456"
        )

        with pytest.raises(ValueError, match="Not enough tickets available"):
            service.purchase_tickets(db_session, purchase, str(test_user.id))

    def test_purchase_tickets_rifa_not_active(self, db_session, test_user):
        """Test purchase for inactive rifa."""
        from app.models.rifa import Rifa

        inactive_rifa = Rifa(
            nombre="Inactive Rifa",
            descripcion="Test",
            precio_ticket=1000,
            numero_ganadores=1,
            estado="cerrada"
        )
        db_session.add(inactive_rifa)
        db_session.commit()

        service = PurchaseService()

        purchase = TicketPurchase(
            rifa_id=str(inactive_rifa.id),
            quantity=1,
            user_id=str(test_user.id),
            idempotency_key="test-key-789"
        )

        with pytest.raises(ValueError, match="Rifa not found or not active"):
            service.purchase_tickets(db_session, purchase, str(test_user.id))

    def test_purchase_tickets_idempotency(self, db_session, test_user, test_rifa, test_tickets):
        """Test idempotent purchases."""
        service = PurchaseService()

        purchase = TicketPurchase(
            rifa_id=str(test_rifa.id),
            quantity=1,
            user_id=str(test_user.id),
            idempotency_key="idempotent-key"
        )

        # Create a mock transaction for idempotency
        from app.models.transaccion import Transaccion
        existing_transaction = Transaccion(
            user_id=str(test_user.id),
            amount=1000,
            currency="COP",
            provider="stripe",
            provider_ref="idempotent-key",
            status="succeeded"
        )
        db_session.add(existing_transaction)
        db_session.commit()

        result = service.purchase_tickets(db_session, purchase, str(test_user.id))

        # Should return existing transaction result
        assert result.transaccion_id == str(existing_transaction.id)

    def test_purchase_tickets_stripe_error(self, db_session, test_user, test_rifa, test_tickets):
        """Test handling of Stripe payment errors."""
        service = PurchaseService()

        purchase = TicketPurchase(
            rifa_id=str(test_rifa.id),
            quantity=1,
            user_id=str(test_user.id),
            idempotency_key="stripe-error-key"
        )

        with patch('stripe.PaymentIntent.create') as mock_stripe_create:
            mock_stripe_create.side_effect = Exception("Stripe error")

            with pytest.raises(ValueError, match="Payment failed"):
                service.purchase_tickets(db_session, purchase, str(test_user.id))