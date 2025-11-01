from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from sqlalchemy.orm import Session
from celery import shared_task
from celery.utils.log import get_task_logger

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.repositories.rifa_repository import RifaRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.integrations.loterias.mock_loteria_service import MockLoteriaService
from app.models.rifa import Rifa
from app.models.ticket import Ticket
from app.models.ganador import Ganador
from app.models.transaccion import Transaccion
import stripe

logger = get_task_logger(__name__)


@shared_task(bind=True, name="app.workers.tasks.close_rifa", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def close_rifa(self, rifa_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Close rifa and determine winners based on lottery results.
    If rifa_id is None, close all expired rifas.
    Includes retries and idempotence checks.
    """
    db: Session = SessionLocal()
    try:
        rifa_repo = RifaRepository()
        ticket_repo = TicketRepository()
        loteria_service = MockLoteriaService()

        if rifa_id:
            rifas_to_close = [rifa_repo.get_by_id(db, rifa_id)]
        else:
            # Get all active rifas that have expired
            expired_rifas = db.query(Rifa).filter(
                Rifa.estado == "activa",
                Rifa.fecha_fin <= datetime.utcnow()
            ).all()
            rifas_to_close = expired_rifas

        results = {"closed_rifas": [], "errors": []}

        for rifa in rifas_to_close:
            if not rifa:
                continue

            # Idempotence check: skip if already closed
            if rifa.estado == "cerrada":
                logger.info(f"Rifa {rifa.id} already closed, skipping")
                continue

            try:
                # Get lottery results for the rifa date
                rifa_date = rifa.fecha_fin.date().isoformat()
                loteria_results = loteria_service.get_results(rifa_date, str(rifa.loteria_id))

                if not loteria_results:
                    logger.warning(f"No lottery results found for rifa {rifa.id} on date {rifa_date}")
                    continue

                # Get all tickets for this rifa
                tickets = ticket_repo.get_tickets_by_rifa(db, str(rifa.id))
                winners = []

                # Determine winners based on lottery results and rifa rules
                for prize_name, winning_number in loteria_results["results"].items():
                    # Find tickets that match the winning number
                    matching_tickets = [t for t in tickets if str(t.numero).zfill(5) == winning_number]

                    for ticket in matching_tickets[:rifa.numero_ganadores]:  # Limit by number of winners
                        winners.append({
                            "ticket_id": str(ticket.id),
                            "numero": ticket.numero,
                            "prize": prize_name,
                            "monto_ganado": calculate_prize_amount(rifa, prize_name)
                        })

                # Check for existing winners to ensure idempotence
                existing_winners = db.query(Ganador).filter(Ganador.ticket_id.in_([w["ticket_id"] for w in winners])).all()
                existing_ticket_ids = {str(g.ticket_id) for g in existing_winners}

                # Mark winners and update ticket status
                for winner in winners:
                    if winner["ticket_id"] in existing_ticket_ids:
                        logger.info(f"Winner for ticket {winner['ticket_id']} already exists, skipping")
                        continue

                    ticket = ticket_repo.update_ticket_status(db, winner["ticket_id"], "ganador")

                    # Create winner record
                    ganador = Ganador(
                        ticket_id=winner["ticket_id"],
                        monto_ganado=winner["monto_ganado"]
                    )
                    db.add(ganador)

                # Update rifa status
                rifa.estado = "cerrada"
                db.commit()

                results["closed_rifas"].append({
                    "rifa_id": str(rifa.id),
                    "winners_count": len(winners),
                    "winners": winners
                })

                logger.info(f"Successfully closed rifa {rifa.id} with {len(winners)} winners")

            except Exception as e:
                logger.error(f"Error closing rifa {rifa.id}: {str(e)}")
                results["errors"].append({
                    "rifa_id": str(rifa.id),
                    "error": str(e)
                })
                db.rollback()

        return results

    finally:
        db.close()


@shared_task(bind=True, name="app.workers.tasks.process_payouts", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def process_payouts(self, rifa_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Process payouts for winners using Stripe.
    If rifa_id is None, process payouts for all closed rifas with unpaid winners.
    """
    db: Session = SessionLocal()
    try:
        transaccion_repo = TransaccionRepository()

        # Get unpaid winners
        if rifa_id:
            winners = db.query(Ganador).join(Ticket).join(Rifa).filter(
                Rifa.id == rifa_id,
                Ganador.fecha_pago.is_(None)
            ).all()
        else:
            winners = db.query(Ganador).filter(
                Ganador.fecha_pago.is_(None)
            ).all()

        results = {"processed_payments": [], "errors": []}

        for winner in winners:
            try:
                # Idempotence check: skip if already paid
                if winner.fecha_pago is not None:
                    logger.info(f"Payout for winner {winner.id} already processed, skipping")
                    continue

                ticket = db.query(Ticket).filter(Ticket.id == winner.ticket_id).first()
                if not ticket or not ticket.usuario_id:
                    continue

                # Get user payment method (assuming stored in transaction)
                transaction = db.query(Transaccion).filter(
                    Transaccion.id == ticket.transaccion_id
                ).first()

                if not transaction:
                    continue

                # Process payout via Stripe
                payout_amount = winner.monto_ganado

                # Create Stripe payout (simplified - in real implementation, use proper Stripe Connect)
                # This is a mock implementation
                payout = {
                    "id": f"payout_{winner.id}",
                    "amount": payout_amount,
                    "status": "succeeded"
                }

                # Update winner with payout info
                winner.fecha_pago = datetime.utcnow()
                winner.referencia_pago = payout["id"]

                # Create payout transaction record
                payout_transaction = Transaccion(
                    user_id=ticket.usuario_id,
                    amount=payout_amount,
                    currency="COP",
                    provider="stripe",
                    provider_ref=payout["id"],
                    status="succeeded"
                )
                db.add(payout_transaction)
                db.commit()

                results["processed_payments"].append({
                    "winner_id": str(winner.id),
                    "amount": payout_amount,
                    "payout_id": payout["id"]
                })

                logger.info(f"Successfully processed payout for winner {winner.id}: {payout_amount} COP")

            except Exception as e:
                logger.error(f"Error processing payout for winner {winner.id}: {str(e)}")
                results["errors"].append({
                    "winner_id": str(winner.id),
                    "error": str(e)
                })
                db.rollback()

        return results

    finally:
        db.close()


@shared_task(bind=True, name="app.workers.tasks.reconcile_loteria")
def reconcile_loteria(self) -> Dict[str, Any]:
    """
    Periodic task to fetch and reconcile lottery results.
    Updates any pending rifas that might have results available.
    """
    db: Session = SessionLocal()
    try:
        loteria_service = MockLoteriaService()
        rifa_repo = RifaRepository()

        # Get active rifas that might need reconciliation
        active_rifas = db.query(Rifa).filter(
            Rifa.estado == "activa",
            Rifa.fecha_fin <= datetime.utcnow() + timedelta(days=1)  # Within last day
        ).all()

        results = {"reconciled_rifas": [], "errors": []}

        for rifa in active_rifas:
            try:
                # Check if lottery results are available
                rifa_date = rifa.fecha_fin.date().isoformat()
                loteria_results = loteria_service.get_results(rifa_date, str(rifa.loteria_id))

                if loteria_results:
                    # Trigger rifa closing if results are available
                    close_result = close_rifa.apply(args=[str(rifa.id)]).get()

                    if close_result and "closed_rifas" in close_result:
                        results["reconciled_rifas"].append({
                            "rifa_id": str(rifa.id),
                            "results_available": True,
                            "closed": True
                        })
                    else:
                        results["reconciled_rifas"].append({
                            "rifa_id": str(rifa.id),
                            "results_available": True,
                            "closed": False
                        })
                else:
                    results["reconciled_rifas"].append({
                        "rifa_id": str(rifa.id),
                        "results_available": False
                    })

            except Exception as e:
                logger.error(f"Error reconciling rifa {rifa.id}: {str(e)}")
                results["errors"].append({
                    "rifa_id": str(rifa.id),
                    "error": str(e)
                })

        logger.info(f"Successfully reconciled {len(results['reconciled_rifas'])} rifas")
        return results

    finally:
        db.close()


def calculate_prize_amount(rifa: Rifa, prize_name: str) -> int:
    """
    Calculate prize amount based on rifa rules and prize type.
    This is a simplified implementation.
    """
    # Base prize amounts (in COP)
    prize_multipliers = {
        "Primer Premio": 0.5,  # 50% of total pot
        "Segundo Premio": 0.3,  # 30% of total pot
        "Tercer Premio": 0.2,  # 20% of total pot
    }

    multiplier = prize_multipliers.get(prize_name, 0.1)  # Default 10%

    # Calculate total pot (simplified - all ticket sales)
    total_tickets = rifa.total_boletas
    ticket_price = 1000  # Assume 1000 COP per ticket

    total_pot = total_tickets * ticket_price
    return int(total_pot * multiplier)