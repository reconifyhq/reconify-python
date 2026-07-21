"""Reconciliations API resource client."""

from __future__ import annotations

from typing import Any

from ..models import (
    CreateReconciliationInputBody,
    ListIntegritySourcesOutputBody,
    ListReconciliationsOutputBody,
    ListSchedulesOutputBody,
    ReconciliationOutputBody,
    ScheduleOutputBody,
    ScheduleRequestBody,
    ScheduleUpdateRequestBody,
)
from .base import AsyncResource, SyncResource


class Reconciliations(SyncResource):
    def list_integrity_sources_for_reconciliation(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/integrity/sources",
            params=query,
            body=None,
            response_model=ListIntegritySourcesOutputBody,
            raw=raw,
        )

    def list_reconciliation_schedules(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliation-schedules",
            params=query,
            body=None,
            response_model=ListSchedulesOutputBody,
            raw=raw,
        )

    def create_reconciliation_schedule(
        self, body: ScheduleRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/reconciliation-schedules",
            params=query,
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    def delete_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "DELETE",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    def get_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    def update_reconciliation_schedule(
        self, id: str, body: ScheduleUpdateRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    def list_reconciliations(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliations",
            params=query,
            body=None,
            response_model=ListReconciliationsOutputBody,
            raw=raw,
        )

    def create_reconciliation(
        self, body: CreateReconciliationInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/reconciliations",
            params=query,
            body=body,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )

    def get_reconciliation(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )


class AsyncReconciliations(AsyncResource):
    async def list_integrity_sources_for_reconciliation(
        self, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "GET",
            "/integrity/sources",
            params=query,
            body=None,
            response_model=ListIntegritySourcesOutputBody,
            raw=raw,
        )

    async def list_reconciliation_schedules(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliation-schedules",
            params=query,
            body=None,
            response_model=ListSchedulesOutputBody,
            raw=raw,
        )

    async def create_reconciliation_schedule(
        self, body: ScheduleRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/reconciliation-schedules",
            params=query,
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    async def delete_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "DELETE",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    async def get_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    async def update_reconciliation_schedule(
        self, id: str, body: ScheduleUpdateRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    async def list_reconciliations(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliations",
            params=query,
            body=None,
            response_model=ListReconciliationsOutputBody,
            raw=raw,
        )

    async def create_reconciliation(
        self, body: CreateReconciliationInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/reconciliations",
            params=query,
            body=body,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )

    async def get_reconciliation(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )


OPERATION_SPECS = {
    "list_integrity_sources_for_reconciliation": ("reconciliations", "GET", "/integrity/sources"),
    "list_reconciliation_schedules": ("reconciliations", "GET", "/reconciliation-schedules"),
    "create_reconciliation_schedule": ("reconciliations", "POST", "/reconciliation-schedules"),
    "delete_reconciliation_schedule": (
        "reconciliations",
        "DELETE",
        "/reconciliation-schedules/{id}",
    ),
    "get_reconciliation_schedule": ("reconciliations", "GET", "/reconciliation-schedules/{id}"),
    "update_reconciliation_schedule": (
        "reconciliations",
        "PATCH",
        "/reconciliation-schedules/{id}",
    ),
    "list_reconciliations": ("reconciliations", "GET", "/reconciliations"),
    "create_reconciliation": ("reconciliations", "POST", "/reconciliations"),
    "get_reconciliation": ("reconciliations", "GET", "/reconciliations/{id}"),
}
