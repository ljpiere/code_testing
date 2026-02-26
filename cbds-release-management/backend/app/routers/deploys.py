from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.deploy_request import DeployRequest
from app.schemas.deploys import (
    DeployListResponse,
    DeployRequestCreate,
    DeployRequestRead,
    DeployRequestUpdate,
)

router = APIRouter(prefix="/deploys", tags=["deploys"])


@router.get("", response_model=DeployListResponse)
def list_deploys(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Busca por JIRA/Proyecto/CHG/OP"),
    environment: str | None = None,
    internal_status: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> DeployListResponse:
    base_query = select(DeployRequest)

    if q:
        like = f"%{q}%"
        base_query = base_query.where(
            or_(
                DeployRequest.jira_ticket.ilike(like),
                DeployRequest.project_name.ilike(like),
                DeployRequest.op_code.ilike(like),
                DeployRequest.servicenow_chg.ilike(like),
            )
        )
    if environment:
        base_query = base_query.where(DeployRequest.environment == environment)
    if internal_status:
        base_query = base_query.where(DeployRequest.internal_status == internal_status)

    total_query = select(func.count()).select_from(base_query.subquery())
    total = db.scalar(total_query) or 0
    rows = list(
        db.scalars(
            base_query.order_by(DeployRequest.created_at.desc()).limit(limit).offset(offset)
        )
    )
    return DeployListResponse(items=rows, total=total)


@router.post("", response_model=DeployRequestRead, status_code=201)
def create_deploy(payload: DeployRequestCreate, db: Session = Depends(get_db)) -> DeployRequest:
    item = DeployRequest(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{deploy_id}", response_model=DeployRequestRead)
def get_deploy(deploy_id: int, db: Session = Depends(get_db)) -> DeployRequest:
    item = db.get(DeployRequest, deploy_id)
    if not item:
        raise HTTPException(status_code=404, detail="Deploy request no encontrado")
    return item


@router.patch("/{deploy_id}", response_model=DeployRequestRead)
def update_deploy(
    deploy_id: int,
    payload: DeployRequestUpdate,
    db: Session = Depends(get_db),
) -> DeployRequest:
    item = db.get(DeployRequest, deploy_id)
    if not item:
        raise HTTPException(status_code=404, detail="Deploy request no encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

