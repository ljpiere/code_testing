from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.connector import ConnectorConfig
from app.schemas.connectors import ConnectorConfigUpsert


def mask_secret(secret: str | None) -> str | None:
    if not secret:
        return None
    if len(secret) <= 6:
        return "*" * len(secret)
    return f"{secret[:2]}{'*' * (len(secret) - 4)}{secret[-2:]}"


def list_connectors(db: Session) -> list[ConnectorConfig]:
    return list(db.scalars(select(ConnectorConfig).order_by(ConnectorConfig.service_name)))


def get_connector(db: Session, service_name: str) -> ConnectorConfig | None:
    return db.scalar(select(ConnectorConfig).where(ConnectorConfig.service_name == service_name))


def upsert_connector(db: Session, payload: ConnectorConfigUpsert) -> ConnectorConfig:
    connector = get_connector(db, payload.service_name)
    if connector is None:
        connector = ConnectorConfig(service_name=payload.service_name)
        db.add(connector)

    connector.base_url = payload.base_url
    connector.username = payload.username
    connector.auth_type = payload.auth_type
    connector.active = payload.active
    connector.extras = payload.extras
    if payload.token is not None:
        connector.token = payload.token

    db.commit()
    db.refresh(connector)
    return connector

