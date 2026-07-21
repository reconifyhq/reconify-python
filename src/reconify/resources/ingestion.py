"""Ingestion API resource client."""

from __future__ import annotations

from typing import Any

from ..models import BatchResponse, IngestEventsInputBody
from .base import AsyncResource, SyncResource


class Ingestion(SyncResource):
    def ingest_integrity_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return self._request(
            "POST",
            "/integrity/events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )

    def ingest_integrity_test_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return self._request(
            "POST",
            "/integrity/test-events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


class AsyncIngestion(AsyncResource):
    async def ingest_integrity_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return await self._request(
            "POST",
            "/integrity/events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )

    async def ingest_integrity_test_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return await self._request(
            "POST",
            "/integrity/test-events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


OPERATION_SPECS = {
    "ingest_integrity_events": ("ingestion", "POST", "/integrity/events"),
    "ingest_integrity_test_events": ("ingestion", "POST", "/integrity/test-events"),
}
