from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func, text
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    nombre = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telefono = Column(String(32), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    rol = Column(Enum("jugador", "admin", "operador", name="user_roles"), default="jugador")
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)