from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.connectors import (
    ConnectorConfigRead,
    ConnectorConfigUpsert,
    ConnectorTestRequest,
    ConnectorTestResponse,
)
from app.services.connector_service import get_connector, list_connectors, mask_secret, upsert_connector
from app.services.jfrog_client import JFrogClient
from app.services.jenkins_client import JenkinsClient
from app.services.servicenow_client import ServiceNowClient

router = APIRouter(prefix="/connectors", tags=["connectors"])


def _to_read_model(row) -> ConnectorConfigRead:
    data = ConnectorConfigRead.model_validate(row)
    data.token_masked = mask_secret(row.token)
    return data


@router.get("", response_model=list[ConnectorConfigRead])
def get_connectors(db: Session = Depends(get_db)) -> list[ConnectorConfigRead]:
    return [_to_read_model(row) for row in list_connectors(db)]


@router.get("/{service_name}", response_model=ConnectorConfigRead)
def get_connector_by_service(service_name: str, db: Session = Depends(get_db)) -> ConnectorConfigRead:
    row = get_connector(db, service_name)
    if not row:
        raise HTTPException(status_code=404, detail="Connector no configurado")
    return _to_read_model(row)


@router.put("/{service_name}", response_model=ConnectorConfigRead)
def put_connector(
    service_name: str,
    payload: ConnectorConfigUpsert,
    db: Session = Depends(get_db),
) -> ConnectorConfigRead:
    if payload.service_name != service_name:
        raise HTTPException(status_code=400, detail="service_name en path y body no coincide")
    row = upsert_connector(db, payload)
    return _to_read_model(row)


@router.post("/test", response_model=ConnectorTestResponse)
def test_connector(payload: ConnectorTestRequest, db: Session = Depends(get_db)) -> ConnectorTestResponse:
    connector = get_connector(db, payload.service_name)
    if not connector:
        return ConnectorTestResponse(
            service_name=payload.service_name,
            ok=False,
            detail="Connector no configurado",
        )
    if not connector.base_url:
        return ConnectorTestResponse(
            service_name=payload.service_name,
            ok=False,
            detail="Falta base_url",
        )

    if payload.service_name == "servicenow":
        client = ServiceNowClient(connector)
        ok, _, detail = client.get_change("CHG0000000")
        return ConnectorTestResponse(
            service_name=payload.service_name,
            ok=ok,
            detail=detail or ("Conectividad OK (respuesta recibida)" if ok else "Error"),
        )

    if payload.service_name == "jfrog":
        client = JFrogClient(connector)
        ok, _, detail = client.build_info("dummy", "0")
        return ConnectorTestResponse(
            service_name=payload.service_name,
            ok=ok,
            detail=detail or ("Conectividad OK (respuesta recibida)" if ok else "Error"),
        )

    if payload.service_name == "jenkins":
        _ = JenkinsClient(connector)
        return ConnectorTestResponse(
            service_name=payload.service_name,
            ok=True,
            detail="Validacion basica OK (base_url configurada).",
        )

    return ConnectorTestResponse(
        service_name=payload.service_name,
        ok=True,
        detail="Connector configurado.",
    )

