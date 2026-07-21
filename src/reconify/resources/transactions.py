"""Transactions API resource client."""

from __future__ import annotations

from typing import Any

from ..models import TransactionOutputBody, TransactionPage
from .base import AsyncResource, SyncResource


class Transactions(SyncResource):
    def list_wallet_transactions(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/transactions",
            params=query,
            body=None,
            response_model=TransactionPage,
            raw=raw,
        )

    def get_wallet_transaction(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/transactions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=TransactionOutputBody,
            raw=raw,
        )


class AsyncTransactions(AsyncResource):
    async def list_wallet_transactions(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/transactions",
            params=query,
            body=None,
            response_model=TransactionPage,
            raw=raw,
        )

    async def get_wallet_transaction(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/transactions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=TransactionOutputBody,
            raw=raw,
        )


OPERATION_SPECS = {
    "list_wallet_transactions": ("transactions", "GET", "/transactions"),
    "get_wallet_transaction": ("transactions", "GET", "/transactions/{id}"),
}
