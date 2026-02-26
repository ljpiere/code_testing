from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.deploy_request import DeployRequest
from app.schemas.integrations import (
    ServiceNowChangeCreateRequest,
    ServiceNowChangeResponse,
    ServiceNowStatusResponse,
)
from app.services.connector_service import get_connector
from app.services.servicenow_client import ServiceNowClient

router = APIRouter(prefix="/servicenow", tags=["servicenow"])


@router.get("/changes/{chg_number}", response_model=ServiceNowStatusResponse)
def get_change_status(chg_number: str, db: Session = Depends(get_db)) -> ServiceNowStatusResponse:
    connector = get_connector(db, "servicenow")
    client = ServiceNowClient(connector)
    ok, raw, detail = client.get_change(chg_number)
    state = raw.get("state") or raw.get("approval") or raw.get("phase")
    return ServiceNowStatusResponse(ok=ok, chg_number=chg_number, state=state, raw=raw, detail=detail)


@router.post("/changes", response_model=ServiceNowChangeResponse)
def create_change(
    payload: ServiceNowChangeCreateRequest,
    db: Session = Depends(get_db),
) -> ServiceNowChangeResponse:
    connector = get_connector(db, "servicenow")
    client = ServiceNowClient(connector)

    body = {
        "short_description": payload.short_description,
        "description": payload.description,
    }
    if payload.assignment_group:
        body["assignment_group"] = payload.assignment_group
    if payload.category:
        body["category"] = payload.category
    if payload.planned_start:
        body["start_date"] = payload.planned_start
    if payload.planned_end:
        body["end_date"] = payload.planned_end
    body.update(payload.extra_fields)

    ok, raw, detail = client.create_change(body)
    chg_number = raw.get("number")
    state = raw.get("state") or raw.get("approval") or raw.get("phase")

    if ok and payload.deploy_request_id:
        deploy = db.get(DeployRequest, payload.deploy_request_id)
        if not deploy:
            raise HTTPException(status_code=404, detail="Deploy request no encontrado")
        deploy.servicenow_chg = chg_number
        deploy.servicenow_status = state
        deploy.internal_status = "change_created"
        db.add(deploy)
        db.commit()

    return ServiceNowChangeResponse(ok=ok, chg_number=chg_number, state=state, raw=raw, detail=detail)


@router.post("/sync/deploy/{deploy_id}", response_model=ServiceNowStatusResponse)
def sync_deploy_chg_status(deploy_id: int, db: Session = Depends(get_db)) -> ServiceNowStatusResponse:
    deploy = db.get(DeployRequest, deploy_id)
    if not deploy:
        raise HTTPException(status_code=404, detail="Deploy request no encontrado")
    if not deploy.servicenow_chg:
        raise HTTPException(status_code=400, detail="Deploy request no tiene CHG asociado")

    connector = get_connector(db, "servicenow")
    client = ServiceNowClient(connector)
    ok, raw, detail = client.get_change(deploy.servicenow_chg)
    state = raw.get("state") or raw.get("approval") or raw.get("phase")
    if ok:
        deploy.servicenow_status = state
        db.add(deploy)
        db.commit()
    return ServiceNowStatusResponse(
        ok=ok,
        chg_number=deploy.servicenow_chg,
        state=state,
        raw=raw,
        detail=detail,
    )

