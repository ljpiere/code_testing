from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.integrations import JFrogBuildLookupRequest, JFrogBuildLookupResponse
from app.services.connector_service import get_connector
from app.services.jfrog_client import JFrogClient

router = APIRouter(prefix="/jfrog", tags=["jfrog"])


@router.post("/builds/lookup", response_model=JFrogBuildLookupResponse)
def lookup_build(payload: JFrogBuildLookupRequest, db: Session = Depends(get_db)) -> JFrogBuildLookupResponse:
    connector = get_connector(db, "jfrog")
    client = JFrogClient(connector)
    ok, raw, detail = client.build_info(payload.build_name, payload.build_number)
    artifact_path = JFrogClient.extract_artifact_path(raw) if ok else None
    return JFrogBuildLookupResponse(
        ok=ok,
        build_name=payload.build_name,
        build_number=payload.build_number,
        artifact_path=artifact_path,
        raw=raw,
        detail=detail,
    )

