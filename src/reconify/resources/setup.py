"""Setup API resource client."""

from __future__ import annotations

from typing import Any

from ..models import (
    BatchResponse,
    CreateSessionRequest,
    CreateSourceRequest,
    SetupIntegrationOutputBody,
    SetupIntegrationsOutputBody,
    SetupSessionOutputBody,
    SetupSourceOutputBody,
    SetupSourcesOutputBody,
    SetupSubmitSessionInputBody,
    UpdateSourceRequest,
)
from .base import AsyncResource, SyncResource


class Setup(SyncResource):
    def list_setup_integrations(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/integrations",
            params=query,
            body=None,
            response_model=SetupIntegrationsOutputBody,
            raw=raw,
        )

    def get_setup_integration(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/integrations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupIntegrationOutputBody,
            raw=raw,
        )

    def list_setup_sources(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/sources",
            params=query,
            body=None,
            response_model=SetupSourcesOutputBody,
            raw=raw,
        )

    def create_setup_source(
        self, body: CreateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/setup/sources",
            params=query,
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    def get_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    def update_setup_source(
        self, id: str, body: UpdateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    def disable_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "DELETE",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    def create_test_session(
        self, body: CreateSessionRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/setup/test-sessions",
            params=query,
            body=body,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def get_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/test-sessions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def get_test_session_result(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/test-sessions/{id}/result",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def retry_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "POST",
            "/setup/test-sessions/{id}/retry",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def submit_test_session_events(
        self,
        id: str,
        body: SetupSubmitSessionInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return self._request(
            "POST",
            "/setup/test-sessions/{id}/submit",
            params={**query, "id": id},
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


class AsyncSetup(AsyncResource):
    async def list_setup_integrations(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/integrations",
            params=query,
            body=None,
            response_model=SetupIntegrationsOutputBody,
            raw=raw,
        )

    async def get_setup_integration(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/integrations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupIntegrationOutputBody,
            raw=raw,
        )

    async def list_setup_sources(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/sources",
            params=query,
            body=None,
            response_model=SetupSourcesOutputBody,
            raw=raw,
        )

    async def create_setup_source(
        self, body: CreateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/setup/sources",
            params=query,
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    async def get_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    async def update_setup_source(
        self, id: str, body: UpdateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    async def disable_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "DELETE",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    async def create_test_session(
        self, body: CreateSessionRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/setup/test-sessions",
            params=query,
            body=body,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def get_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/test-sessions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def get_test_session_result(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/test-sessions/{id}/result",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def retry_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "POST",
            "/setup/test-sessions/{id}/retry",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def submit_test_session_events(
        self,
        id: str,
        body: SetupSubmitSessionInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return await self._request(
            "POST",
            "/setup/test-sessions/{id}/submit",
            params={**query, "id": id},
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


OPERATION_SPECS = {
    "list_setup_integrations": ("setup", "GET", "/setup/integrations"),
    "get_setup_integration": ("setup", "GET", "/setup/integrations/{id}"),
    "list_setup_sources": ("setup", "GET", "/setup/sources"),
    "create_setup_source": ("setup", "POST", "/setup/sources"),
    "get_setup_source": ("setup", "GET", "/setup/sources/{id}"),
    "update_setup_source": ("setup", "PATCH", "/setup/sources/{id}"),
    "disable_setup_source": ("setup", "DELETE", "/setup/sources/{id}"),
    "create_test_session": ("setup", "POST", "/setup/test-sessions"),
    "get_test_session": ("setup", "GET", "/setup/test-sessions/{id}"),
    "get_test_session_result": ("setup", "GET", "/setup/test-sessions/{id}/result"),
    "retry_test_session": ("setup", "POST", "/setup/test-sessions/{id}/retry"),
    "submit_test_session_events": ("setup", "POST", "/setup/test-sessions/{id}/submit"),
}
