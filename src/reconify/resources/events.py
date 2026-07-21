"""Events API resource client."""

from __future__ import annotations

from typing import Any

from ..models import EventDetail, EventPage, EventRevealOutputBody
from .base import AsyncResource, SyncResource


class Events(SyncResource):
    def list_events(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/events",
            params=query,
            body=None,
            response_model=EventPage,
            raw=raw,
        )

    def get_event(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/events/{id}",
            params={**query, "id": id},
            body=None,
            response_model=EventDetail,
            raw=raw,
        )

    def reveal_event_field(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/events/{id}/reveal",
            params={**query, "id": id},
            body=None,
            response_model=EventRevealOutputBody,
            raw=raw,
        )


class AsyncEvents(AsyncResource):
    async def list_events(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/events",
            params=query,
            body=None,
            response_model=EventPage,
            raw=raw,
        )

    async def get_event(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/events/{id}",
            params={**query, "id": id},
            body=None,
            response_model=EventDetail,
            raw=raw,
        )

    async def reveal_event_field(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/events/{id}/reveal",
            params={**query, "id": id},
            body=None,
            response_model=EventRevealOutputBody,
            raw=raw,
        )


OPERATION_SPECS = {
    "list_events": ("events", "GET", "/events"),
    "get_event": ("events", "GET", "/events/{id}"),
    "reveal_event_field": ("events", "GET", "/events/{id}/reveal"),
}
