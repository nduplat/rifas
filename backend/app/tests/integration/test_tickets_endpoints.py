import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app


@pytest.mark.asyncio
class TestTicketsEndpoints:
    async def test_read_tickets_unauthorized(self, db_session):
        """Test reading tickets without authentication."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/api/v1/tickets/")
            assert response.status_code == 401

    async def test_purchase_tickets_success(self, db_session, test_user, test_rifa, test_tickets):
        """Test successful ticket purchase."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # First login to get token
            login_data = {
                "username": test_user.email,
                "password": "testpass"  # From conftest fixture
            }
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]

            headers = {"Authorization": f"Bearer {token}"}

            purchase_data = {
                "rifa_id": str(test_rifa.id),
                "quantity": 2,
                "user_id": str(test_user.id),
                "idempotency_key": "test-purchase-key"
            }

            # Mock Stripe for testing
            import stripe
            with pytest.mock.patch('stripe.PaymentIntent.create') as mock_create, \
                 pytest.mock.patch('stripe.PaymentIntent.confirm') as mock_confirm:

                mock_payment_intent = pytest.mock.Mock()
                mock_payment_intent.id = "pi_test_123"
                mock_create.return_value = mock_payment_intent

                response = await client.post("/api/v1/tickets/purchase", json=purchase_data, headers=headers)
                assert response.status_code == 200

                data = response.json()
                assert "tickets" in data
                assert "transaccion_id" in data
                assert len(data["tickets"]) == 2

    async def test_purchase_tickets_insufficient_quantity(self, db_session, test_user, test_rifa):
        """Test purchase with insufficient tickets."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            purchase_data = {
                "rifa_id": str(test_rifa.id),
                "quantity": 100,  # More than available
                "user_id": str(test_user.id),
                "idempotency_key": "insufficient-key"
            }

            response = await client.post("/api/v1/tickets/purchase", json=purchase_data, headers=headers)
            assert response.status_code == 400
            assert "Not enough tickets available" in response.json()["detail"]

    async def test_read_user_tickets(self, db_session, test_user, test_rifa, test_tickets):
        """Test reading user's tickets."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Assign some tickets to user
            for ticket in test_tickets[:3]:
                ticket.usuario_id = str(test_user.id)
                ticket.estado = "vendido"
            db_session.commit()

            # Login
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            response = await client.get("/api/v1/tickets/", headers=headers)
            assert response.status_code == 200

            data = response.json()
            assert len(data) == 3
            assert all(ticket["usuario_id"] == str(test_user.id) for ticket in data)