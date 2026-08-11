"""Events API resource client."""

from __future__ import annotations

from typing import Any

from ..models import Event, ListEventsResponse
from .base import AsyncResource, SyncResource


class Events(SyncResource):
    def list_events(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/events", params=query, response_model=ListEventsResponse, raw=raw
        )

    def get_event(self, event_id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/events/{event_id}",
            params={**query, "event_id": event_id},
            response_model=Event,
            raw=raw,
        )

    def list_issue_events(self, issue_id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues/{issue_id}/events",
            params={**query, "issue_id": issue_id},
            response_model=ListEventsResponse,
            raw=raw,
        )


class AsyncEvents(AsyncResource):
    async def list_events(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/events", params=query, response_model=ListEventsResponse, raw=raw
        )

    async def get_event(self, event_id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/events/{event_id}",
            params={**query, "event_id": event_id},
            response_model=Event,
            raw=raw,
        )

    async def list_issue_events(self, issue_id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues/{issue_id}/events",
            params={**query, "issue_id": issue_id},
            response_model=ListEventsResponse,
            raw=raw,
        )
