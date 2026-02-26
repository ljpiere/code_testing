from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.models.base import Base


class DeployRequest(Base):
    __tablename__ = "deploy_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    jira_ticket: Mapped[str] = mapped_column(String(50), index=True)
    project_name: Mapped[str] = mapped_column(String(150), index=True)
    module_name: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    op_code: Mapped[str] = mapped_column(String(100), index=True)
    environment: Mapped[str] = mapped_column(String(20), default="prod", index=True)
    pipeline_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    technical_description: Mapped[str] = mapped_column(Text)
    impacted_jobs: Mapped[list[str]] = mapped_column(JSON, default=list)
    impacted_tables: Mapped[list[str]] = mapped_column(JSON, default=list)
    build_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    jfrog_artifact: Mapped[str | None] = mapped_column(String(500), nullable=True)
    change_description: Mapped[str] = mapped_column(Text)
    impact_if_not_deployed: Mapped[str] = mapped_column(Text)
    deploy_technical_steps: Mapped[str] = mapped_column(Text)
    requested_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    servicenow_chg: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    servicenow_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    internal_status: Mapped[str] = mapped_column(String(50), default="draft", index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

