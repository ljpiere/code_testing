from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.models.base import Base


class ConnectorConfig(Base):
    __tablename__ = "connector_configs"
    __table_args__ = (UniqueConstraint("service_name", name="uq_connector_service_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(String(50), index=True)
    base_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
    username: Mapped[str | None] = mapped_column(String(200), nullable=True)
    token: Mapped[str | None] = mapped_column(Text, nullable=True)
    auth_type: Mapped[str] = mapped_column(String(30), default="basic")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    extras: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

