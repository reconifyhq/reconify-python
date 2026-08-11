"""Public API metadata resource."""

from __future__ import annotations

from typing import Any

from ..models import APIInfo, Health
from .base import AsyncResource, SyncResource


class Metadata(SyncResource):
    def get_api_info(self, raw: bool = False, **query: Any) -> Any:
        return self._request("GET", "", params=query, response_model=APIInfo, raw=raw)

    def get_health(self, raw: bool = False, **query: Any) -> Any:
        return self._request("GET", "/health", params=query, response_model=Health, raw=raw)


class AsyncMetadata(AsyncResource):
    async def get_api_info(self, raw: bool = False, **query: Any) -> Any:
        return await self._request("GET", "", params=query, response_model=APIInfo, raw=raw)

    async def get_health(self, raw: bool = False, **query: Any) -> Any:
        return await self._request("GET", "/health", params=query, response_model=Health, raw=raw)
