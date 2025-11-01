from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Ganador(Base):
    __tablename__ = "ganadores"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False)
    monto_ganado = Column(Integer, nullable=False)
    fecha_pago = Column(DateTime(timezone=True), nullable=True)
    referencia_pago = Column(String(255))