from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func, text
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(8), default="COP")
    provider = Column(String(50))  # stripe, sandbox...
    provider_ref = Column(String(255))
    idempotency_key = Column(String(255), unique=True, nullable=False)
    status = Column(Enum("pending", "succeeded", "failed", "refunded", name="trans_status"), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())