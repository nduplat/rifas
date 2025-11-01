from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import random

from app.api.v1.deps import get_db, get_current_operador_user, get_current_active_user
from app.models.rifa import Rifa
from app.models.ticket import Ticket
from app.models.ganador import Ganador
from app.schemas.rifa import RifaOut, RifaCreate, RifaUpdate, RifaList
from app.schemas.ticket import TicketPurchase, TicketPurchaseResponse
from app.services.purchase_service import PurchaseService
from app.services.rifa_service import RifaService
from app.core.rate_limiting import purchase_limiter
from app.core.logging import audit_logger

router = APIRouter()


@router.get("/", response_model=List[RifaList])
def read_rifas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    rifas = db.query(Rifa).offset(skip).limit(limit).all()
    return rifas


@router.post("/", response_model=RifaOut)
def create_rifa(
    rifa_in: RifaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    db_rifa = Rifa(**rifa_in.dict())
    db.add(db_rifa)
    db.commit()
    db.refresh(db_rifa)
    return db_rifa


@router.get("/{rifa_id}", response_model=RifaOut)
def read_rifa(
    rifa_id: str,
    db: Session = Depends(get_db)
):
    rifa = db.query(Rifa).filter(Rifa.id == rifa_id).first()
    if rifa is None:
        raise HTTPException(status_code=404, detail="Rifa not found")
    return rifa


@router.put("/{rifa_id}", response_model=RifaOut)
def update_rifa(
    rifa_id: str,
    rifa_in: RifaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    rifa = db.query(Rifa).filter(Rifa.id == rifa_id).first()
    if rifa is None:
        raise HTTPException(status_code=404, detail="Rifa not found")

    update_data = rifa_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rifa, field, value)

    db.commit()
    db.refresh(rifa)
    return rifa


@router.delete("/{rifa_id}")
def delete_rifa(
    rifa_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    rifa = db.query(Rifa).filter(Rifa.id == rifa_id).first()
    if rifa is None:
        raise HTTPException(status_code=404, detail="Rifa not found")

    db.delete(rifa)
    db.commit()
    return {"message": "Rifa deleted successfully"}


@router.post("/{rifa_id}/close")
def close_rifa(
    rifa_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    rifa_service = RifaService(db)
    return rifa_service.close_rifa(rifa_id)


@router.post("/{rifa_id}/recalculate")
def recalculate_rifa(
    rifa_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    rifa_service = RifaService(db)
    return rifa_service.recalculate_rifa(rifa_id)


@router.post("/{rifa_id}/cerrar")
def cerrar_rifa(
    rifa_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    rifa_service = RifaService(db)
    return rifa_service.close_rifa(rifa_id)


@router.post("/{rifa_id}/recalcular")
def recalcular_rifa(
    rifa_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    rifa_service = RifaService(db)
    return rifa_service.recalculate_rifa(rifa_id)


@router.post("/{rifa_id}/tickets", response_model=TicketPurchaseResponse)
@purchase_limiter.limit("10 per minute")
async def purchase_tickets_for_rifa(
    request: Request,
    rifa_id: str,
    purchase: TicketPurchase,
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    # Verify rifa_id matches
    if str(purchase.rifa_id) != rifa_id:
        raise HTTPException(status_code=400, detail="Rifa ID mismatch")

    # Verify user
    if str(purchase.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Cannot purchase for other users")

    # Audit log the purchase attempt
    audit_logger.info(
        "rifa_purchase_attempt",
        user_id=str(current_user.id),
        rifa_id=rifa_id,
        quantity=purchase.quantity,
        idempotency_key=purchase.idempotency_key,
        ip_address=request.client.host if request.client else None
    )

    try:
        purchase_service = PurchaseService()
        result = await purchase_service.purchase_tickets(db, purchase, str(current_user.id))

        # Audit log successful purchase
        audit_logger.info(
            "rifa_purchase_success",
            user_id=str(current_user.id),
            rifa_id=rifa_id,
            quantity=purchase.quantity,
            transaction_id=result.transaccion_id,
            ticket_count=len(result.tickets)
        )

        return result
    except ValueError as e:
        # Audit log failed purchase
        audit_logger.warning(
            "rifa_purchase_failed",
            user_id=str(current_user.id),
            rifa_id=rifa_id,
            quantity=purchase.quantity,
            error=str(e)
        )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Audit log system error
        audit_logger.error(
            "rifa_purchase_error",
            user_id=str(current_user.id),
            rifa_id=rifa_id,
            quantity=purchase.quantity,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")
