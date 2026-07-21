"""Ledger API resource client."""

from __future__ import annotations

from typing import Any

from ..models import (
    CreateSourceInputBody,
    IngestTransactionsInputBody,
    IngestTransactionsOutputBody,
    ListPeriodsOutputBody,
    ListSourcesOutputBody,
    ListTransactionsOutputBody,
    SourceOutputBody,
    UpdateSourceInputBody,
)
from .base import AsyncResource, SyncResource


class Ledger(SyncResource):
    def list_ledger_sources(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources",
            params=query,
            body=None,
            response_model=ListSourcesOutputBody,
            raw=raw,
        )

    def create_ledger_source(
        self, body: CreateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/ledger/sources",
            params=query,
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    def delete_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "DELETE",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    def get_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SourceOutputBody,
            raw=raw,
        )

    def update_ledger_source(
        self, id: str, body: UpdateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    def list_source_periods(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources/{id}/periods",
            params={**query, "id": id},
            body=None,
            response_model=ListPeriodsOutputBody,
            raw=raw,
        )

    def list_transactions(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=None,
            response_model=ListTransactionsOutputBody,
            raw=raw,
        )

    def ingest_transactions(
        self, id: str, body: IngestTransactionsInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=body,
            response_model=IngestTransactionsOutputBody,
            raw=raw,
        )


class AsyncLedger(AsyncResource):
    async def list_ledger_sources(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources",
            params=query,
            body=None,
            response_model=ListSourcesOutputBody,
            raw=raw,
        )

    async def create_ledger_source(
        self, body: CreateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/ledger/sources",
            params=query,
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    async def delete_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "DELETE",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    async def get_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SourceOutputBody,
            raw=raw,
        )

    async def update_ledger_source(
        self, id: str, body: UpdateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    async def list_source_periods(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources/{id}/periods",
            params={**query, "id": id},
            body=None,
            response_model=ListPeriodsOutputBody,
            raw=raw,
        )

    async def list_transactions(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=None,
            response_model=ListTransactionsOutputBody,
            raw=raw,
        )

    async def ingest_transactions(
        self, id: str, body: IngestTransactionsInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=body,
            response_model=IngestTransactionsOutputBody,
            raw=raw,
        )


OPERATION_SPECS = {
    "list_ledger_sources": ("ledger", "GET", "/ledger/sources"),
    "create_ledger_source": ("ledger", "POST", "/ledger/sources"),
    "delete_ledger_source": ("ledger", "DELETE", "/ledger/sources/{id}"),
    "get_ledger_source": ("ledger", "GET", "/ledger/sources/{id}"),
    "update_ledger_source": ("ledger", "PATCH", "/ledger/sources/{id}"),
    "list_source_periods": ("ledger", "GET", "/ledger/sources/{id}/periods"),
    "list_transactions": ("ledger", "GET", "/ledger/sources/{id}/transactions"),
    "ingest_transactions": ("ledger", "POST", "/ledger/sources/{id}/transactions"),
}
