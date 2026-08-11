"""Monitoring event ingestion resource client."""

from __future__ import annotations

from typing import Any

from ..models import MonitoringBatchRequest, MonitoringBatchResponse
from .base import AsyncResource, SyncResource


class Ingestion(SyncResource):
    def ingest_monitoring_events(
        self, body: MonitoringBatchRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/events",
            params=query,
            body=body,
            response_model=MonitoringBatchResponse,
            raw=raw,
        )


class AsyncIngestion(AsyncResource):
    async def ingest_monitoring_events(
        self, body: MonitoringBatchRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/events",
            params=query,
            body=body,
            response_model=MonitoringBatchResponse,
            raw=raw,
        )
