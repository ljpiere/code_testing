from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.integrations import JenkinsTriggerRequest, JenkinsTriggerResponse
from app.services.connector_service import get_connector
from app.services.jenkins_client import JenkinsClient

router = APIRouter(prefix="/jenkins", tags=["jenkins"])


@router.post("/jobs/trigger", response_model=JenkinsTriggerResponse)
def trigger_job(payload: JenkinsTriggerRequest, db: Session = Depends(get_db)) -> JenkinsTriggerResponse:
    connector = get_connector(db, "jenkins")
    client = JenkinsClient(connector)
    ok, queue_url, detail = client.trigger_job(payload.job_path, payload.parameters)
    return JenkinsTriggerResponse(ok=ok, queue_url=queue_url, detail=detail)

