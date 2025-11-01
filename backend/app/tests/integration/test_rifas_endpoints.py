import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app


@pytest.mark.asyncio
class TestRifasEndpoints:
    async def test_read_rifas(self, db_session, test_rifa):
        """Test reading rifas list."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/api/v1/rifas/")
            assert response.status_code == 200

            data = response.json()
            assert len(data) >= 1
            assert any(rifa["id"] == str(test_rifa.id) for rifa in data)

    async def test_read_rifa_by_id(self, db_session, test_rifa):
        """Test reading specific rifa."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get(f"/api/v1/rifas/{test_rifa.id}")
            assert response.status_code == 200

            data = response.json()
            assert data["id"] == str(test_rifa.id)
            assert data["nombre"] == test_rifa.nombre

    async def test_read_rifa_not_found(self, db_session):
        """Test reading non-existent rifa."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/api/v1/rifas/non-existent-id")
            assert response.status_code == 404
            assert "Rifa not found" in response.json()["detail"]

    async def test_create_rifa_unauthorized(self, db_session):
        """Test creating rifa without proper authorization."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            rifa_data = {
                "nombre": "Test Rifa",
                "descripcion": "Test description",
                "precio_ticket": 1000,
                "numero_ganadores": 1
            }

            response = await client.post("/api/v1/rifas/", json=rifa_data)
            assert response.status_code == 401

    async def test_close_rifa_success(self, db_session, test_user, test_rifa, test_tickets):
        """Test closing a rifa successfully."""
        # Create operador user
        from app.models.user import User
        from app.core.security import get_password_hash

        operador = User(
            nombre="Operador Test",
            email="operador@example.com",
            telefono="1234567890",
            hashed_password=get_password_hash("testpass"),
            rol="operador"
        )
        db_session.add(operador)
        db_session.commit()

        # Sell some tickets
        for ticket in test_tickets[:5]:
            ticket.usuario_id = str(test_user.id)
            ticket.estado = "vendido"
        db_session.commit()

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login as operador
            login_data = {"username": operador.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            response = await client.post(f"/api/v1/rifas/{test_rifa.id}/close", headers=headers)
            assert response.status_code == 200

            data = response.json()
            assert "message" in data
            assert "winners" in data
            assert len(data["winners"]) == test_rifa.numero_ganadores

    async def test_close_rifa_insufficient_tickets(self, db_session):
        """Test closing rifa with insufficient sold tickets."""
        from app.models.user import User
        from app.models.rifa import Rifa
        from app.core.security import get_password_hash

        operador = User(
            nombre="Operador Test",
            email="operador2@example.com",
            telefono="1234567890",
            hashed_password=get_password_hash("testpass"),
            rol="operador"
        )
        db_session.add(operador)

        rifa = Rifa(
            nombre="Insufficient Rifa",
            descripcion="Test",
            precio_ticket=1000,
            numero_ganadores=5,  # Requires 5 winners
            estado="activa"
        )
        db_session.add(rifa)
        db_session.commit()

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login as operador
            login_data = {"username": operador.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            response = await client.post(f"/api/v1/rifas/{rifa.id}/close", headers=headers)
            assert response.status_code == 400
            assert "Not enough tickets sold" in response.json()["detail"]

    async def test_close_rifa_unauthorized(self, db_session, test_rifa):
        """Test closing rifa without proper authorization."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Try to close without authentication
            response = await client.post(f"/api/v1/rifas/{test_rifa.id}/close")
            assert response.status_code == 401

    async def test_close_rifa_wrong_role(self, db_session, test_user, test_rifa):
        """Test closing rifa with wrong user role."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login as regular user (not operador)
            login_data = {"username": test_user.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            response = await client.post(f"/api/v1/rifas/{test_rifa.id}/close", headers=headers)
            assert response.status_code == 403  # Forbidden

    async def test_close_rifa_already_closed(self, db_session):
        """Test closing a rifa that's already closed."""
        from app.models.user import User
        from app.models.rifa import Rifa
        from app.core.security import get_password_hash

        operador = User(
            nombre="Operador Test",
            email="operador3@example.com",
            telefono="1234567890",
            hashed_password=get_password_hash("testpass"),
            rol="operador"
        )
        db_session.add(operador)

        closed_rifa = Rifa(
            nombre="Already Closed Rifa",
            descripcion="Already closed",
            precio_ticket=1000,
            numero_ganadores=1,
            estado="cerrada"
        )
        db_session.add(closed_rifa)
        db_session.commit()

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login as operador
            login_data = {"username": operador.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            response = await client.post(f"/api/v1/rifas/{closed_rifa.id}/close", headers=headers)
            assert response.status_code == 400
            assert "Rifa is not active" in response.json()["detail"]

    async def test_close_rifa_not_found(self, db_session):
        """Test closing a non-existent rifa."""
        from app.models.user import User
        from app.core.security import get_password_hash

        operador = User(
            nombre="Operador Test",
            email="operador4@example.com",
            telefono="1234567890",
            hashed_password=get_password_hash("testpass"),
            rol="operador"
        )
        db_session.add(operador)
        db_session.commit()

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Login as operador
            login_data = {"username": operador.email, "password": "testpass"}
            login_response = await client.post("/api/v1/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            response = await client.post("/api/v1/rifas/non-existent-id/close", headers=headers)
            assert response.status_code == 404
            assert "Rifa not found" in response.json()["detail"]