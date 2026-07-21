"""Search API resource client."""

from __future__ import annotations

from typing import Any

from ..models import SearchPage
from .base import AsyncResource, SyncResource


class Search(SyncResource):
    def search_integrity_resources(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/search",
            params=query,
            body=None,
            response_model=SearchPage,
            raw=raw,
        )


class AsyncSearch(AsyncResource):
    async def search_integrity_resources(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/search",
            params=query,
            body=None,
            response_model=SearchPage,
            raw=raw,
        )


OPERATION_SPECS = {
    "search_integrity_resources": ("search", "GET", "/search"),
}
