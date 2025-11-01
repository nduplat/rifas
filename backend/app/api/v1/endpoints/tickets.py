from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db, get_current_active_user
from app.models.ticket import Ticket
from app.services.purchase_service import PurchaseService
from app.schemas.ticket import TicketOut, TicketPurchase, TicketPurchaseResponse
from app.core.rate_limiting import purchase_limiter
from app.core.logging import audit_logger

router = APIRouter()


@router.get("/", response_model=List[TicketOut])
def read_tickets(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    tickets = db.query(Ticket).filter(Ticket.usuario_id == current_user.id).offset(skip).limit(limit).all()
    return tickets


@router.post("/purchase", response_model=TicketPurchaseResponse)
@purchase_limiter.limit("10 per minute")
async def purchase_tickets(
    request: Request,
    purchase: TicketPurchase,
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    # Verify user
    if str(purchase.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Cannot purchase for other users")

    # Audit log the purchase attempt
    audit_logger.info(
        "purchase_attempt",
        user_id=str(current_user.id),
        rifa_id=str(purchase.rifa_id),
        quantity=purchase.quantity,
        idempotency_key=purchase.idempotency_key,
        ip_address=request.client.host if request.client else None
    )

    try:
        purchase_service = PurchaseService()
        result = await purchase_service.purchase_tickets(db, purchase, str(current_user.id))

        # Audit log successful purchase
        audit_logger.info(
            "purchase_success",
            user_id=str(current_user.id),
            rifa_id=str(purchase.rifa_id),
            quantity=purchase.quantity,
            transaction_id=result.transaccion_id,
            ticket_count=len(result.tickets)
        )

        return result
    except ValueError as e:
        # Audit log failed purchase
        audit_logger.warning(
            "purchase_failed",
            user_id=str(current_user.id),
            rifa_id=str(purchase.rifa_id),
            quantity=purchase.quantity,
            error=str(e)
        )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Audit log system error
        audit_logger.error(
            "purchase_error",
            user_id=str(current_user.id),
            rifa_id=str(purchase.rifa_id),
            quantity=purchase.quantity,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")
