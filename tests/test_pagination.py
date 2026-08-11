from __future__ import annotations

import httpx

from reconify import AsyncReconify, Reconify


def _event(event_id: str) -> dict[str, object]:
    return {
        "id": event_id,
        "flow": "payment_to_wallet",
        "event_type": "payment.succeeded",
        "reference": event_id,
        "entity_type": "wallet",
        "entity_id": "wallet-1",
        "occurred_at": "2026-01-01T00:00:00Z",
        "received_at": "2026-01-01T00:00:01Z",
        "status": "processed",
    }


def test_sync_cursor_iterator_forwards_query_and_cursor() -> None:
    requests: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        requests.append(params)
        if "after" not in params:
            return httpx.Response(
                200,
                json={"events": [_event("event-1")], "limit": 1, "next_cursor": "cursor-1"},
                request=request,
            )
        return httpx.Response(
            200,
            json={"events": [_event("event-2")], "limit": 1},
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
                json={"events": [_event("event-1")], "limit": 1, "next_cursor": "cursor-1"},
                request=request,
            )
        return httpx.Response(
            200, json={"events": [_event("event-2")], "limit": 1}, request=request
        )

    async with AsyncReconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as client:
        events = [event async for event in client.iter_events(limit=1)]

    assert [event.id for event in events] == ["event-1", "event-2"]
    assert requests == [{"limit": "1"}, {"after": "cursor-1", "limit": "1"}]
