from typing import Any

import httpx

from app.core.config import get_settings
from app.models.connector import ConnectorConfig


class ServiceNowClient:
    def __init__(self, connector: ConnectorConfig | None) -> None:
        self.connector = connector
        self.settings = get_settings()

    def _auth_kwargs(self) -> dict[str, Any]:
        if not self.connector:
            return {}
        if self.connector.auth_type == "basic" and self.connector.username and self.connector.token:
            return {"auth": (self.connector.username, self.connector.token)}
        if self.connector.auth_type == "bearer" and self.connector.token:
            return {"headers": {"Authorization": f"Bearer {self.connector.token}"}}
        if self.connector.auth_type == "api_key" and self.connector.token:
            header_name = self.connector.extras.get("api_key_header", "X-API-Key")
            return {"headers": {header_name: self.connector.token}}
        return {}

    def _url(self, path: str) -> str:
        base = (self.connector.base_url if self.connector and self.connector.base_url else "").rstrip("/")
        return f"{base}/{path.lstrip('/')}"

    def get_change(self, chg_number: str) -> tuple[bool, dict[str, Any], str | None]:
        if not self.connector or not self.connector.base_url:
            return False, {}, "Connector de ServiceNow no configurado."

        query = f"number={chg_number}"
        url = self._url(f"api/now/table/change_request?sysparm_query={query}")
        try:
            with httpx.Client(timeout=self.settings.request_timeout_seconds, **self._auth_kwargs()) as client:
                response = client.get(url)
                response.raise_for_status()
                payload = response.json()
                result = payload.get("result") or []
                row = result[0] if result else {}
                return True, row, None
        except Exception as exc:  # pragma: no cover
            return False, {}, str(exc)

    def create_change(self, body: dict[str, Any]) -> tuple[bool, dict[str, Any], str | None]:
        if not self.connector or not self.connector.base_url:
            return False, {}, "Connector de ServiceNow no configurado."

        url = self._url("api/now/table/change_request")
        try:
            with httpx.Client(timeout=self.settings.request_timeout_seconds, **self._auth_kwargs()) as client:
                response = client.post(url, json=body)
                response.raise_for_status()
                payload = response.json()
                result = payload.get("result") or {}
                return True, result, None
        except Exception as exc:  # pragma: no cover
            return False, {}, str(exc)

