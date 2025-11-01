from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db, get_current_operador_user
from app.models.loteria import Loteria
from app.schemas.loteria import LoteriaOut, LoteriaCreate, LoteriaUpdate

router = APIRouter()


@router.get("/", response_model=List[LoteriaOut])
def read_loterias(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    loterias = db.query(Loteria).offset(skip).limit(limit).all()
    return loterias


@router.post("/", response_model=LoteriaOut)
def create_loteria(
    loteria_in: LoteriaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    db_loteria = Loteria(**loteria_in.dict())
    db.add(db_loteria)
    db.commit()
    db.refresh(db_loteria)
    return db_loteria


@router.get("/{loteria_id}", response_model=LoteriaOut)
def read_loteria(
    loteria_id: str,
    db: Session = Depends(get_db)
):
    loteria = db.query(Loteria).filter(Loteria.id == loteria_id).first()
    if loteria is None:
        raise HTTPException(status_code=404, detail="Loteria not found")
    return loteria


@router.put("/{loteria_id}", response_model=LoteriaOut)
def update_loteria(
    loteria_id: str,
    loteria_in: LoteriaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    loteria = db.query(Loteria).filter(Loteria.id == loteria_id).first()
    if loteria is None:
        raise HTTPException(status_code=404, detail="Loteria not found")

    update_data = loteria_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(loteria, field, value)

    db.commit()
    db.refresh(loteria)
    return loteria


@router.delete("/{loteria_id}")
def delete_loteria(
    loteria_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    loteria = db.query(Loteria).filter(Loteria.id == loteria_id).first()
    if loteria is None:
        raise HTTPException(status_code=404, detail="Loteria not found")

    db.delete(loteria)
    db.commit()
    return {"message": "Loteria deleted successfully"}
