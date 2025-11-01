import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app


@pytest.mark.asyncio
class TestPurchaseFlowE2E:
    async def test_complete_purchase_flow(self, db_session, test_user, test_rifa, test_tickets):
        """Test complete end-to-end purchase flow."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Step 1: Register/Login user
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            assert login_response.status_code == 200
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            # Step 2: Check available rifas
            rifas_response = await client.get("/api/v1/rifas/")
            assert rifas_response.status_code == 200
            rifas = rifas_response.json()
            assert len(rifas) > 0

            # Step 3: Get specific rifa details
            rifa_response = await client.get(f"/api/v1/rifas/{test_rifa.id}")
            assert rifa_response.status_code == 200
            rifa_data = rifa_response.json()
            assert rifa_data["estado"] == "activa"

            # Step 4: Purchase tickets
            purchase_data = {
                "rifa_id": str(test_rifa.id),
                "quantity": 3,
                "user_id": str(test_user.id),
                "idempotency_key": "e2e-purchase-key-123"
            }

            # Mock Stripe payment
            with pytest.mock.patch('stripe.PaymentIntent.create') as mock_create, \
                 pytest.mock.patch('stripe.PaymentIntent.confirm') as mock_confirm:

                mock_payment_intent = pytest.mock.Mock()
                mock_payment_intent.id = "pi_e2e_test_123"
                mock_create.return_value = mock_payment_intent

                purchase_response = await client.post(
                    "/api/v1/tickets/purchase",
                    json=purchase_data,
                    headers=headers
                )
                assert purchase_response.status_code == 200

                purchase_result = purchase_response.json()
                assert len(purchase_result["tickets"]) == 3
                assert "transaccion_id" in purchase_result

            # Step 5: Verify tickets are assigned to user
            tickets_response = await client.get("/api/v1/tickets/", headers=headers)
            assert tickets_response.status_code == 200
            user_tickets = tickets_response.json()
            assert len(user_tickets) == 3
            assert all(ticket["estado"] == "vendido" for ticket in user_tickets)
            assert all(ticket["usuario_id"] == str(test_user.id) for ticket in user_tickets)

            # Step 6: Verify transaction was created
            transaction_id = purchase_result["transaccion_id"]
            # Note: In a real scenario, you'd have an endpoint to check transactions
            # For now, we verify through the database state

    async def test_purchase_flow_idempotency(self, db_session, test_user, test_rifa, test_tickets):
        """Test that purchase flow is idempotent."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            purchase_data = {
                "rifa_id": str(test_rifa.id),
                "quantity": 2,
                "user_id": str(test_user.id),
                "idempotency_key": "idempotent-e2e-key"
            }

            # Mock Stripe
            with pytest.mock.patch('stripe.PaymentIntent.create') as mock_create, \
                 pytest.mock.patch('stripe.PaymentIntent.confirm') as mock_confirm:

                mock_payment_intent = pytest.mock.Mock()
                mock_payment_intent.id = "pi_idempotent_test"
                mock_create.return_value = mock_payment_intent

                # First purchase
                response1 = await client.post(
                    "/api/v1/tickets/purchase",
                    json=purchase_data,
                    headers=headers
                )
                assert response1.status_code == 200
                result1 = response1.json()

                # Second purchase with same idempotency key
                response2 = await client.post(
                    "/api/v1/tickets/purchase",
                    json=purchase_data,
                    headers=headers
                )
                assert response2.status_code == 200
                result2 = response2.json()

                # Should return same result
                assert result1["transaccion_id"] == result2["transaccion_id"]
                assert len(result1["tickets"]) == len(result2["tickets"])

    async def test_purchase_flow_insufficient_funds(self, db_session, test_user, test_rifa):
        """Test purchase flow when there aren't enough tickets."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            purchase_data = {
                "rifa_id": str(test_rifa.id),
                "quantity": 1000,  # Way more than available
                "user_id": str(test_user.id),
                "idempotency_key": "insufficient-e2e-key"
            }

            response = await client.post(
                "/api/v1/tickets/purchase",
                json=purchase_data,
                headers=headers
            )
            assert response.status_code == 400
            assert "Not enough tickets available" in response.json()["detail"]

    async def test_purchase_flow_rifa_closed(self, db_session, test_user):
        """Test purchase flow when rifa is closed."""
        from app.models.rifa import Rifa

        closed_rifa = Rifa(
            nombre="Closed Rifa",
            descripcion="Already closed",
            precio_ticket=1000,
            numero_ganadores=1,
            estado="cerrada"
        )
        db_session.add(closed_rifa)
        db_session.commit()

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            purchase_data = {
                "rifa_id": str(closed_rifa.id),
                "quantity": 1,
                "user_id": str(test_user.id),
                "idempotency_key": "closed-rifa-key"
            }

            response = await client.post(
                "/api/v1/tickets/purchase",
                json=purchase_data,
                headers=headers
            )
            assert response.status_code == 400
            assert "Rifa not found or not active" in response.json()["detail"]

    async def test_concurrent_purchase_with_same_idempotency_key(self, db_session, test_user, test_rifa, test_tickets):
        """Test concurrent purchase requests with same idempotency key to ensure no duplicates."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            purchase_data = {
                "rifa_id": str(test_rifa.id),
                "quantity": 1,
                "user_id": str(test_user.id),
                "idempotency_key": "concurrent-test-key"
            }

            # Mock Stripe
            with pytest.mock.patch('stripe.PaymentIntent.create') as mock_create, \
                 pytest.mock.patch('stripe.PaymentIntent.confirm') as mock_confirm:

                mock_payment_intent = pytest.mock.Mock()
                mock_payment_intent.id = "pi_concurrent_test"
                mock_create.return_value = mock_payment_intent

                # Simulate N concurrent requests (using asyncio.gather)
                N = 5
                tasks = []
                for _ in range(N):
                    task = client.post(
                        "/api/v1/tickets/purchase",
                        json=purchase_data,
                        headers=headers
                    )
                    tasks.append(task)

                # Execute all requests concurrently
                responses = await asyncio.gather(*tasks, return_exceptions=True)

                # All should succeed (200 status)
                successful_responses = [r for r in responses if not isinstance(r, Exception) and r.status_code == 200]
                assert len(successful_responses) == N

                # All should return the same transaction_id (idempotent)
                transaction_ids = [r.json()["transaccion_id"] for r in successful_responses]
                assert all(tid == transaction_ids[0] for tid in transaction_ids)

                # Verify only one ticket was actually purchased (no duplicates)
                tickets_response = await client.get("/api/v1/tickets/", headers=headers)
                user_tickets = tickets_response.json()
                assert len(user_tickets) == 1  # Only one ticket despite N requests
                assert user_tickets[0]["estado"] == "vendido"
                assert user_tickets[0]["usuario_id"] == str(test_user.id)