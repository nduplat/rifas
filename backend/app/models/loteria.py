from sqlalchemy import Column, String, Text
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from .base import Base


class Loteria(Base):
    __tablename__ = "loterias"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    frecuencia = Column(String)  # diaria, semanal...
    url_resultados = Column(String)
    meta = Column(JSONB, default={})