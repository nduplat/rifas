from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    rifa_id = Column(UUID(as_uuid=True), ForeignKey("rifas.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    numero = Column(Integer, nullable=False)
    comprado_en = Column(DateTime(timezone=True))
    estado = Column(Enum("disponible", "vendido", "ganador", "anulado", name="ticket_states"), default="disponible")
    precio = Column(Integer)
    transaccion_id = Column(UUID(as_uuid=True), nullable=True)