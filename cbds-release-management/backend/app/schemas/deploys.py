from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DeployRequestBase(BaseModel):
    jira_ticket: str = Field(..., examples=["CBDS-1234"])
    project_name: str
    module_name: str | None = None
    op_code: str
    environment: str = Field(default="prod", examples=["dev", "staging", "prod"])
    pipeline_name: str | None = None
    technical_description: str
    impacted_jobs: list[str] = Field(default_factory=list)
    impacted_tables: list[str] = Field(default_factory=list)
    build_number: str | None = None
    jfrog_artifact: str | None = None
    change_description: str
    impact_if_not_deployed: str
    deploy_technical_steps: str
    requested_by: str | None = None
    servicenow_chg: str | None = None
    servicenow_status: str | None = None
    internal_status: str = "draft"
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class DeployRequestCreate(DeployRequestBase):
    pass


class DeployRequestUpdate(BaseModel):
    jira_ticket: str | None = None
    project_name: str | None = None
    module_name: str | None = None
    op_code: str | None = None
    environment: str | None = None
    pipeline_name: str | None = None
    technical_description: str | None = None
    impacted_jobs: list[str] | None = None
    impacted_tables: list[str] | None = None
    build_number: str | None = None
    jfrog_artifact: str | None = None
    change_description: str | None = None
    impact_if_not_deployed: str | None = None
    deploy_technical_steps: str | None = None
    requested_by: str | None = None
    servicenow_chg: str | None = None
    servicenow_status: str | None = None
    internal_status: str | None = None
    metadata_json: dict[str, Any] | None = None


class DeployRequestRead(DeployRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeployListResponse(BaseModel):
    items: list[DeployRequestRead]
    total: int

