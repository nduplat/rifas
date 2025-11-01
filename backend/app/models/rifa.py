from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey
from sqlalchemy.sql import func, text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from .base import Base


class Rifa(Base):
    __tablename__ = "rifas"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    nombre = Column(String(255), nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categoria_rifa.id"))
    loteria_id = Column(UUID(as_uuid=True), ForeignKey("loterias.id"))
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin = Column(DateTime(timezone=True), index=True)
    numero_ganadores = Column(Integer, default=1)
    estado = Column(Enum("pendiente", "activa", "cerrada", "cancelada", name="rifa_states"), default="pendiente")
    reglas = Column(JSONB, default={})  # reglas paramétricas: ganar_dos_primeros, reparto, ...
    total_boletas = Column(Integer, default=100)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())