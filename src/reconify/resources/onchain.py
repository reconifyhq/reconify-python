"""On-chain evidence source registration resource client."""

from __future__ import annotations

from typing import Any

from ..errors import ReconifyValidationError
from ..models import OnchainSourceRequest, OnchainSourceResponse
from .base import AsyncResource, SyncResource


class Onchain(SyncResource):
    def register_onchain_source(
        self,
        body: OnchainSourceRequest,
        *,
        idempotency_key: str,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        if not idempotency_key or len(idempotency_key) > 200:
            raise ReconifyValidationError("idempotency_key must be between 1 and 200 characters")
        return self._request(
            "POST",
            "/onchain-sources",
            params=query,
            body=body,
            response_model=OnchainSourceResponse,
            raw=raw,
            headers={"Idempotency-Key": idempotency_key},
        )

    register_source = register_onchain_source


class AsyncOnchain(AsyncResource):
    async def register_onchain_source(
        self,
        body: OnchainSourceRequest,
        *,
        idempotency_key: str,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        if not idempotency_key or len(idempotency_key) > 200:
            raise ReconifyValidationError("idempotency_key must be between 1 and 200 characters")
        return await self._request(
            "POST",
            "/onchain-sources",
            params=query,
            body=body,
            response_model=OnchainSourceResponse,
            raw=raw,
            headers={"Idempotency-Key": idempotency_key},
        )

    register_source = register_onchain_source
