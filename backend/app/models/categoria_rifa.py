from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class CategoriaRifa(Base):
    __tablename__ = "categoria_rifa"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    nombre = Column(String, nullable=False, unique=True)
    color = Column(String(32))
    valor_boleta = Column(Integer, nullable=False)
    total_recaudo = Column(Integer)
    rake = Column(Numeric(5, 4))  # 0.25
    fondo_premios = Column(Integer)
    premio_por_ganador = Column(Integer)
    comentario = Column(String(255))