import pytest
from sqlalchemy.orm import Session

from app.repositories.ticket_repository import TicketRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.rifa_repository import RifaRepository


class TestTicketRepository:
    def test_get_available_tickets(self, db_session, test_rifa, test_tickets):
        """Test getting available tickets."""
        repo = TicketRepository()

        available = repo.get_available_tickets(db_session, str(test_rifa.id), limit=5)
        assert len(available) == 5
        assert all(ticket.estado == "disponible" for ticket in available)

    def test_get_available_tickets_with_lock(self, db_session, test_rifa, test_tickets):
        """Test getting available tickets with lock."""
        repo = TicketRepository()

        available = repo.get_available_tickets_with_lock(db_session, str(test_rifa.id), limit=3)
        assert len(available) == 3
        assert all(ticket.estado == "disponible" for ticket in available)

    def test_get_tickets_by_user(self, db_session, test_user, test_rifa, test_tickets):
        """Test getting tickets by user."""
        repo = TicketRepository()

        # First assign some tickets to user
        tickets_to_assign = test_tickets[:2]
        for ticket in tickets_to_assign:
            ticket.usuario_id = str(test_user.id)
            ticket.estado = "vendido"
        db_session.commit()

        user_tickets = repo.get_tickets_by_user(db_session, str(test_user.id))
        assert len(user_tickets) == 2
        assert all(ticket.usuario_id == str(test_user.id) for ticket in user_tickets)

    def test_get_next_ticket_number(self, db_session, test_rifa, test_tickets):
        """Test getting next ticket number."""
        repo = TicketRepository()

        next_number = repo.get_next_ticket_number(db_session, str(test_rifa.id))
        assert next_number == 11  # Since we have tickets 1-10

    def test_bulk_update_tickets(self, db_session, test_user, test_rifa, test_tickets):
        """Test bulk updating tickets."""
        repo = TicketRepository()

        ticket_ids = [str(ticket.id) for ticket in test_tickets[:3]]
        updates = {
            "estado": "vendido",
            "usuario_id": str(test_user.id)
        }

        repo.bulk_update_tickets(db_session, ticket_ids, updates)

        # Verify updates
        for ticket_id in ticket_ids:
            ticket = repo.get_by_id(db_session, ticket_id)
            assert ticket.estado == "vendido"
            assert ticket.usuario_id == str(test_user.id)


class TestTransaccionRepository:
    def test_get_by_idempotency_key(self, db_session, test_user):
        """Test getting transaction by idempotency key."""
        repo = TransaccionRepository()

        from app.models.transaccion import Transaccion
        transaction = Transaccion(
            user_id=str(test_user.id),
            amount=1000,
            currency="COP",
            provider="stripe",
            provider_ref="test-idempotency-key",
            status="pending"
        )
        db_session.add(transaction)
        db_session.commit()

        found = repo.get_by_idempotency_key(db_session, "test-idempotency-key")
        assert found is not None
        assert found.provider_ref == "test-idempotency-key"

    def test_get_user_transactions(self, db_session, test_user):
        """Test getting user transactions."""
        repo = TransaccionRepository()

        from app.models.transaccion import Transaccion
        transactions = []
        for i in range(3):
            transaction = Transaccion(
                user_id=str(test_user.id),
                amount=1000 * (i + 1),
                currency="COP",
                provider="stripe",
                provider_ref=f"ref-{i}",
                status="succeeded"
            )
            transactions.append(transaction)
            db_session.add(transaction)
        db_session.commit()

        user_transactions = repo.get_user_transactions(db_session, str(test_user.id))
        assert len(user_transactions) == 3
        assert all(t.user_id == str(test_user.id) for t in user_transactions)


class TestRifaRepository:
    def test_get_active_rifa(self, db_session):
        """Test getting active rifa."""
        repo = RifaRepository()

        from app.models.rifa import Rifa
        active_rifa = Rifa(
            nombre="Active Rifa",
            descripcion="Test",
            precio_ticket=1000,
            numero_ganadores=1,
            estado="activa"
        )
        inactive_rifa = Rifa(
            nombre="Inactive Rifa",
            descripcion="Test",
            precio_ticket=1000,
            numero_ganadores=1,
            estado="cerrada"
        )
        db_session.add(active_rifa)
        db_session.add(inactive_rifa)
        db_session.commit()

        found_active = repo.get_active_rifa(db_session, str(active_rifa.id))
        found_inactive = repo.get_active_rifa(db_session, str(inactive_rifa.id))

        assert found_active is not None
        assert found_active.estado == "activa"
        assert found_inactive is None

    def test_get_rifa_with_tickets_count(self, db_session, test_rifa, test_tickets):
        """Test getting rifa with available tickets count."""
        repo = RifaRepository()

        # Mark some tickets as sold
        for ticket in test_tickets[:3]:
            ticket.estado = "vendido"
        db_session.commit()

        rifa_with_count = repo.get_rifa_with_tickets_count(db_session, str(test_rifa.id))
        assert rifa_with_count is not None
        assert rifa_with_count.available_tickets == 7  # 10 total - 3 sold