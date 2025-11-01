import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings


@pytest.mark.asyncio
class TestAuthEndpoints:
    async def test_register_user(self, db_session):
        """Test user registration endpoint."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            user_data = {
                "nombre": "Test User",
                "email": "test@example.com",
                "telefono": "1234567890",
                "password": "testpass123",
                "rol": "usuario"
            }

            response = await client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 200

            data = response.json()
            assert data["email"] == user_data["email"]
            assert data["nombre"] == user_data["nombre"]
            assert "id" in data
            assert "hashed_password" not in data

    async def test_register_duplicate_email(self, db_session):
        """Test registering with duplicate email."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            user_data = {
                "nombre": "Test User",
                "email": "duplicate@example.com",
                "telefono": "1234567890",
                "password": "testpass123",
                "rol": "usuario"
            }

            # First registration
            response1 = await client.post("/api/v1/auth/register", json=user_data)
            assert response1.status_code == 200

            # Second registration with same email
            response2 = await client.post("/api/v1/auth/register", json=user_data)
            assert response2.status_code == 400
            assert "Email already registered" in response2.json()["detail"]

    async def test_login_success(self, db_session):
        """Test successful login."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # First register a user
            user_data = {
                "nombre": "Login Test User",
                "email": "login@example.com",
                "telefono": "1234567890",
                "password": "testpass123",
                "rol": "usuario"
            }
            await client.post("/api/v1/auth/register", json=user_data)

            # Now login
            login_data = {
                "username": "login@example.com",
                "password": "testpass123"
            }

            response = await client.post("/api/v1/auth/login", data=login_data)
            assert response.status_code == 200

            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

    async def test_login_invalid_credentials(self, db_session):
        """Test login with invalid credentials."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            login_data = {
                "username": "nonexistent@example.com",
                "password": "wrongpass"
            }

            response = await client.post("/api/v1/auth/login", data=login_data)
            assert response.status_code == 401
            assert "Incorrect email or password" in response.json()["detail"]

    async def test_login_missing_fields(self, db_session):
        """Test login with missing required fields."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Missing password
            login_data = {"username": "test@example.com"}
            response = await client.post("/api/v1/auth/login", data=login_data)
            assert response.status_code == 422  # Validation error

            # Missing username
            login_data = {"password": "testpass"}
            response = await client.post("/api/v1/auth/login", data=login_data)
            assert response.status_code == 422  # Validation error

    async def test_register_missing_fields(self, db_session):
        """Test registration with missing required fields."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Missing email
            user_data = {
                "nombre": "Test User",
                "telefono": "1234567890",
                "password": "testpass123",
                "rol": "usuario"
            }
            response = await client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 422

            # Missing password
            user_data = {
                "nombre": "Test User",
                "email": "test@example.com",
                "telefono": "1234567890",
                "rol": "usuario"
            }
            response = await client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 422

    async def test_register_invalid_email(self, db_session):
        """Test registration with invalid email format."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            user_data = {
                "nombre": "Test User",
                "email": "invalid-email",
                "telefono": "1234567890",
                "password": "testpass123",
                "rol": "usuario"
            }
            response = await client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 422

    async def test_register_weak_password(self, db_session):
        """Test registration with weak password."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            user_data = {
                "nombre": "Test User",
                "email": "weakpass@example.com",
                "telefono": "1234567890",
                "password": "123",  # Too short
                "rol": "usuario"
            }
            response = await client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 422

    async def test_login_case_sensitive_email(self, db_session):
        """Test login with case-sensitive email."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Register with lowercase email
            user_data = {
                "nombre": "Case Test User",
                "email": "casetest@example.com",
                "telefono": "1234567890",
                "password": "testpass123",
                "rol": "usuario"
            }
            await client.post("/api/v1/auth/register", json=user_data)

            # Try login with uppercase email
            login_data = {
                "username": "CASETEST@EXAMPLE.COM",
                "password": "testpass123"
            }
            response = await client.post("/api/v1/auth/login", data=login_data)
            assert response.status_code == 401  # Should fail due to case sensitivity