"""Wallets API resource client."""

from __future__ import annotations

from typing import Any

from ..models import WalletBalanceOutputBody, WalletOutputBody, WalletPage
from .base import AsyncResource, SyncResource


class Wallets(SyncResource):
    def list_wallets(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/wallets",
            params=query,
            body=None,
            response_model=WalletPage,
            raw=raw,
        )

    def get_wallet(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/wallets/{id}",
            params={**query, "id": id},
            body=None,
            response_model=WalletOutputBody,
            raw=raw,
        )

    def get_wallet_balance(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/wallets/{id}/balance",
            params={**query, "id": id},
            body=None,
            response_model=WalletBalanceOutputBody,
            raw=raw,
        )


class AsyncWallets(AsyncResource):
    async def list_wallets(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/wallets",
            params=query,
            body=None,
            response_model=WalletPage,
            raw=raw,
        )

    async def get_wallet(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/wallets/{id}",
            params={**query, "id": id},
            body=None,
            response_model=WalletOutputBody,
            raw=raw,
        )

    async def get_wallet_balance(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/wallets/{id}/balance",
            params={**query, "id": id},
            body=None,
            response_model=WalletBalanceOutputBody,
            raw=raw,
        )


OPERATION_SPECS = {
    "list_wallets": ("wallets", "GET", "/wallets"),
    "get_wallet": ("wallets", "GET", "/wallets/{id}"),
    "get_wallet_balance": ("wallets", "GET", "/wallets/{id}/balance"),
}
