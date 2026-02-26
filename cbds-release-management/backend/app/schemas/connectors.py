from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


ServiceName = Literal["confluence", "jenkins", "servicenow", "servicenow_db", "jfrog", "jira"]
AuthType = Literal["basic", "bearer", "api_key", "none"]


class ConnectorConfigBase(BaseModel):
    service_name: ServiceName
    base_url: str | None = None
    username: str | None = None
    auth_type: AuthType = "basic"
    active: bool = True
    extras: dict[str, Any] = Field(default_factory=dict)


class ConnectorConfigUpsert(ConnectorConfigBase):
    token: str | None = Field(
        default=None,
        description="Access token or password. Stored for MVP; use Vault/KMS in production.",
    )


class ConnectorConfigRead(ConnectorConfigBase):
    id: int
    token_masked: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConnectorTestRequest(BaseModel):
    service_name: ServiceName


class ConnectorTestResponse(BaseModel):
    service_name: ServiceName
    ok: bool
    detail: str

