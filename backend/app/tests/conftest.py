import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

from app.db.session import Base
from app.core.config import settings
from app.main import app


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


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user."""
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        nombre="Test User",
        email="test@example.com",
        telefono="1234567890",
        hashed_password=get_password_hash("testpass"),
        rol="usuario"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_rifa(db_session):
    """Create a test rifa."""
    from app.models.rifa import Rifa

    rifa = Rifa(
        nombre="Test Rifa",
        descripcion="Test description",
        precio_ticket=1000,
        numero_ganadores=1,
        estado="activa"
    )
    db_session.add(rifa)
    db_session.commit()
    db_session.refresh(rifa)
    return rifa


@pytest.fixture(scope="function")
def test_tickets(db_session, test_rifa):
    """Create test tickets for a rifa."""
    from app.models.ticket import Ticket

    tickets = []
    for i in range(10):
        ticket = Ticket(
            rifa_id=str(test_rifa.id),
            numero=i + 1,
            estado="disponible"
        )
        tickets.append(ticket)
        db_session.add(ticket)
    db_session.commit()
    for ticket in tickets:
        db_session.refresh(ticket)
    return tickets


@pytest.fixture(scope="function")
async def async_client():
    """Create async test client."""
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client