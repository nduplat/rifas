import pytest
import os
from httpx import AsyncClient
from sqlalchemy.orm import Session

# Set environment variables for testing
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['SECRET_KEY'] = 'supersecretkeythatislongenoughforrequirements'
os.environ['STRIPE_SECRET_KEY'] = 'sk_test_dummy'
os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_dummy'
os.environ['STRIPE_WEBHOOK_SECRET'] = 'whsec_dummy'

from app.main import app
from app.db.session import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Create test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.mark.asyncio
class TestCategoriaEndpoints:
    async def test_create_and_list_categorias(self, db_session):
        """Test creating a categoria and listing categorias."""
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            # Create a categoria
            categoria_data = {
                "nombre": "Test Categoria",
                "valor_boleta": 1000,
                "color": "#FF0000",
                "total_recaudo": 10000,
                "rake": 0.05,
                "fondo_premios": 9500,
                "premio_por_ganador": 4750,
                "comentario": "Test categoria"
            }

            response = await client.post("/api/v1/categorias/", json=categoria_data)
            assert response.status_code == 200

            data = response.json()
            assert data["nombre"] == categoria_data["nombre"]
            assert data["valor_boleta"] == categoria_data["valor_boleta"]
            assert "id" in data

            # List categorias
            response = await client.get("/api/v1/categorias/")
            assert response.status_code == 200

            data = response.json()
            assert isinstance(data, list)
            assert len(data) >= 1
            assert any(c["nombre"] == categoria_data["nombre"] for c in data)