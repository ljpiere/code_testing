from typing import Any

import httpx

from app.core.config import get_settings
from app.models.connector import ConnectorConfig


class JFrogClient:
    def __init__(self, connector: ConnectorConfig | None) -> None:
        self.connector = connector
        self.settings = get_settings()

    def _headers(self) -> dict[str, str]:
        if not self.connector or not self.connector.token:
            return {}
        if self.connector.auth_type == "bearer":
            return {"Authorization": f"Bearer {self.connector.token}"}
        if self.connector.auth_type == "api_key":
            header_name = self.connector.extras.get("api_key_header", "X-JFrog-Art-Api")
            return {header_name: self.connector.token}
        return {}

    def _auth(self) -> tuple[str, str] | None:
        if not self.connector:
            return None
        if self.connector.auth_type == "basic" and self.connector.username and self.connector.token:
            return (self.connector.username, self.connector.token)
        return None

    def build_info(self, build_name: str, build_number: str) -> tuple[bool, dict[str, Any], str | None]:
        if not self.connector or not self.connector.base_url:
            return False, {}, "Connector de JFrog no configurado."

        url = self.connector.base_url.rstrip("/") + f"/api/build/{build_name}/{build_number}"
        kwargs: dict[str, Any] = {"headers": self._headers(), "timeout": self.settings.request_timeout_seconds}
        auth = self._auth()
        if auth:
            kwargs["auth"] = auth

        try:
            with httpx.Client() as client:
                response = client.get(url, **kwargs)
                response.raise_for_status()
                return True, response.json(), None
        except Exception as exc:  # pragma: no cover
            return False, {}, str(exc)

    @staticmethod
    def extract_artifact_path(payload: dict[str, Any]) -> str | None:
        build_info = payload.get("buildInfo") or {}
        modules = build_info.get("modules") or []
        for module in modules:
            artifacts = module.get("artifacts") or []
            for artifact in artifacts:
                name = artifact.get("name")
                if name:
                    repo = artifact.get("repo") or artifact.get("repoKey") or ""
                    path = artifact.get("path") or ""
                    return "/".join(part.strip("/") for part in [repo, path, name] if part)
        return None

