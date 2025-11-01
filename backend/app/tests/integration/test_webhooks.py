import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.config import settings
from app.db.session import get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db():
    return Mock(spec=AsyncSession)


def test_stripe_webhook_success(client, mock_db):
    """Test successful Stripe webhook handling."""
    # Mock the database dependency
    app.dependency_overrides[get_db] = lambda: mock_db

    # Mock Stripe webhook payload
    payload = {
        "id": "evt_test_webhook",
        "object": "event",
        "api_version": "2020-08-27",
        "created": 1326853478,
        "data": {
            "object": {
                "id": "pi_test_payment_intent",
                "object": "payment_intent",
                "amount": 1000,
                "currency": "cop",
                "status": "succeeded"
            }
        },
        "livemode": False,
        "pending_webhooks": 1,
        "request": {
            "id": "req_test_request",
            "idempotency_key": None
        },
        "type": "payment_intent.succeeded"
    }

    # Mock Stripe signature
    sig_header = "t=1492774577,v1=test_signature"

    with patch('app.services.stripe_service.StripeService.construct_event') as mock_construct:
        mock_event = Mock()
        mock_event.__getitem__.side_effect = lambda key: payload[key]
        mock_construct.return_value = mock_event

        with patch('app.api.v1.endpoints.webhooks.handle_stripe_event') as mock_handle:
            response = client.post(
                "/api/v1/webhooks/stripe",
                json=payload,
                headers={"stripe-signature": sig_header}
            )

            assert response.status_code == 200
            assert response.json() == {"status": "success"}
            mock_construct.assert_called_once()
            mock_handle.assert_called_once()


def test_stripe_webhook_invalid_signature(client):
    """Test webhook with invalid signature."""
    payload = {"test": "data"}
    sig_header = "invalid_signature"

    with patch('app.services.stripe_service.StripeService.construct_event') as mock_construct:
        mock_construct.side_effect = Exception("Invalid signature")

        response = client.post(
            "/api/v1/webhooks/stripe",
            json=payload,
            headers={"stripe-signature": sig_header}
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]


def test_stripe_webhook_missing_signature(client):
    """Test webhook without signature header."""
    payload = {"test": "data"}

    response = client.post("/api/v1/webhooks/stripe", json=payload)

    assert response.status_code == 400
    assert "Missing Stripe signature header" in response.json()["detail"]