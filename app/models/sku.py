from sqlalchemy import String, Integer, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class SKU(Base):
    __tablename__ = "skus"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    inventory = relationship("Inventory", back_populates="sku")

Index("ix_skus_code", SKU.code)
