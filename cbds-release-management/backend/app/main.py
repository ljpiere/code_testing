from fastapi import FastAPI

from app.core.config import get_settings
from app.core.cors import configure_cors
from app.db import create_db_and_tables
from app.routers import connectors, deploys, jfrog, jenkins, servicenow

settings = get_settings()

app = FastAPI(title=settings.app_name)
configure_cors(app, settings.allowed_origins)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(deploys.router, prefix=settings.api_prefix)
app.include_router(connectors.router, prefix=settings.api_prefix)
app.include_router(servicenow.router, prefix=settings.api_prefix)
app.include_router(jfrog.router, prefix=settings.api_prefix)
app.include_router(jenkins.router, prefix=settings.api_prefix)

