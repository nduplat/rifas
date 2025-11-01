from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.v1.deps import get_db, get_current_operador_user
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaOut, CategoriaCreate

router = APIRouter()


@router.get("/", response_model=List[CategoriaOut])
def read_categorias(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    return categorias


@router.post("/", response_model=CategoriaOut)
def create_categoria(
    categoria_in: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_operador_user)
):
    try:
        db_categoria = Categoria(**categoria_in.dict())
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        return db_categoria
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria with this name already exists"
        )