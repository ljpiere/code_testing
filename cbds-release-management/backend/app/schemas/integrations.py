from typing import Any

from pydantic import BaseModel, Field


class ServiceNowChangeCreateRequest(BaseModel):
    deploy_request_id: int | None = None
    short_description: str
    description: str
    assignment_group: str | None = None
    category: str | None = None
    planned_start: str | None = None
    planned_end: str | None = None
    extra_fields: dict[str, Any] = Field(default_factory=dict)


class ServiceNowChangeResponse(BaseModel):
    ok: bool
    chg_number: str | None = None
    state: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
    detail: str | None = None


class ServiceNowStatusResponse(BaseModel):
    ok: bool
    chg_number: str
    state: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
    detail: str | None = None


class JFrogBuildLookupRequest(BaseModel):
    build_name: str
    build_number: str


class JFrogBuildLookupResponse(BaseModel):
    ok: bool
    build_name: str
    build_number: str
    artifact_path: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
    detail: str | None = None


class JenkinsTriggerRequest(BaseModel):
    job_path: str = Field(..., examples=["folder/pipeline-prod"])
    parameters: dict[str, Any] = Field(default_factory=dict)


class JenkinsTriggerResponse(BaseModel):
    ok: bool
    queue_url: str | None = None
    detail: str | None = None

