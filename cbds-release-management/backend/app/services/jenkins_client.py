from typing import Any
from urllib.parse import quote

import httpx

from app.core.config import get_settings
from app.models.connector import ConnectorConfig


class JenkinsClient:
    def __init__(self, connector: ConnectorConfig | None) -> None:
        self.connector = connector
        self.settings = get_settings()

    def _headers(self) -> dict[str, str]:
        if not self.connector:
            return {}
        crumb_value = self.connector.extras.get("crumb")
        crumb_field = self.connector.extras.get("crumb_field")
        headers: dict[str, str] = {}
        if crumb_value and crumb_field:
            headers[crumb_field] = crumb_value
        return headers

    def _auth(self) -> tuple[str, str] | None:
        if not self.connector:
            return None
        if self.connector.username and self.connector.token:
            return (self.connector.username, self.connector.token)
        return None

    def trigger_job(self, job_path: str, parameters: dict[str, Any]) -> tuple[bool, str | None, str | None]:
        if not self.connector or not self.connector.base_url:
            return False, None, "Connector de Jenkins no configurado."

        job_segments = [f"job/{quote(segment)}" for segment in job_path.split("/") if segment]
        endpoint = "buildWithParameters" if parameters else "build"
        url = self.connector.base_url.rstrip("/") + "/" + "/".join(job_segments) + f"/{endpoint}"
        kwargs: dict[str, Any] = {
            "headers": self._headers(),
            "timeout": self.settings.request_timeout_seconds,
        }
        auth = self._auth()
        if auth:
            kwargs["auth"] = auth
        if parameters:
            kwargs["params"] = parameters

        try:
            with httpx.Client() as client:
                response = client.post(url, **kwargs)
                if response.status_code not in (200, 201, 202):
                    return False, None, f"HTTP {response.status_code}: {response.text}"
                return True, response.headers.get("Location"), None
        except Exception as exc:  # pragma: no cover
            return False, None, str(exc)

