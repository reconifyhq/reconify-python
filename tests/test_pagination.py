from __future__ import annotations

import httpx

from reconify import AsyncReconify, Reconify


def _event(event_id: str) -> dict[str, object]:
    return {
        "amountMinor": 100,
        "applied": True,
        "canonicalHash": f"hash-{event_id}",
        "currency": "USD",
        "eventSchemaVersion": 1,
        "eventType": "payment",
        "id": event_id,
        "occurredAt": "2026-01-01T00:00:00Z",
        "processingStatus": "applied",
        "receivedAt": "2026-01-01T00:00:01Z",
        "sourceEventId": f"source-{event_id}",
        "sourceId": "source-1",
    }


def test_sync_cursor_iterator_forwards_query_and_cursor() -> None:
    requests: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        requests.append(params)
        if "after" not in params:
            return httpx.Response(
                200,
                json={"events": [_event("event-1")], "limit": 1, "nextCursor": "cursor-1"},
                request=request,
            )
        return httpx.Response(
            200,
            json={"events": [_event("event-2")], "limit": 1, "nextCursor": None},
            request=request,
        )

    with Reconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        events = list(client.iter_events(limit=1))

    assert [event.id for event in events] == ["event-1", "event-2"]
    assert requests == [{"limit": "1"}, {"after": "cursor-1", "limit": "1"}]


async def test_async_cursor_iterator_forwards_query_and_cursor() -> None:
    requests: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        requests.append(params)
        if "after" not in params:
            return httpx.Response(
                200,
                json={"events": [_event("event-1")], "limit": 1, "nextCursor": "cursor-1"},
                request=request,
            )
        return httpx.Response(
            200,
            json={"events": [_event("event-2")], "limit": 1, "nextCursor": None},
            request=request,
        )

    async with AsyncReconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as client:
        events = [event async for event in client.iter_events(limit=1)]

    assert [event.id for event in events] == ["event-1", "event-2"]
    assert requests == [{"limit": "1"}, {"after": "cursor-1", "limit": "1"}]
