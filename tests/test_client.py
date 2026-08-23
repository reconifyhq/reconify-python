from __future__ import annotations

import json

import httpx
import pytest

from reconify import Reconify
from reconify.errors import (
    ReconifyAuthenticationError,
    ReconifyConflictError,
    ReconifyNotFoundError,
    ReconifyPermissionError,
    ReconifyRateLimitError,
    ReconifyRequestError,
    ReconifyServiceUnavailableError,
)
from reconify.models import (
    AddNoteRequest,
    MonitoringBatchRequest,
    MonitoringEvent,
    PatchIssueRequest,
)
from reconify.transport import RetryConfig


def _event(event_id: str = "evt_1") -> dict[str, object]:
    return {
        "id": event_id,
        "flow": "payment_to_wallet",
        "event_type": "payment.succeeded",
        "reference": "order-1",
        "entity_type": "wallet",
        "entity_id": "wallet-1",
        "occurred_at": "2026-01-01T00:00:00Z",
        "received_at": "2026-01-01T00:00:01Z",
        "status": "processed",
    }


def test_base_url_and_request_contract() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200, json=_event(), headers={"X-Request-ID": "response-id"}, request=request
        )

    with Reconify(
        "rk_test",
        base_url="http://localhost:3002/v2/",
        request_id="caller-id",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        result = client.events.get_event("event id")

    assert result.id == "evt_1"
    assert str(requests[0].url) == "http://localhost:3002/v2/events/event%20id"
    assert requests[0].headers["Authorization"] == "Bearer rk_test"
    assert requests[0].headers["X-Request-ID"] == "caller-id"


def test_base_url_and_key_can_come_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RECONIFY_API_URL", "http://api.test/v2/")
    monkeypatch.setenv("RECONIFY_API_KEY", "rk_environment")
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"status": "operational"}, request=request)

    with Reconify(http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.metadata.get_health()

    assert str(requests[0].url) == "http://api.test/v2/health"
    assert requests[0].headers["Authorization"] == "Bearer rk_environment"


def test_ingestion_serializes_typed_body() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(202, json={"results": []}, request=request)

    body = MonitoringBatchRequest(
        events=[
            MonitoringEvent(
                flow="payment_to_wallet",
                type="payment.succeeded",
                reference="order-1",
                entity_id="wallet-1",
                amount="10.00",
                correlation_id="checkout-123",
                currency="USD",
            )
        ]
    )
    with Reconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        client.ingestion.ingest_monitoring_events(body)

    assert json.loads(requests[0].content)["events"][0]["entity_id"] == "wallet-1"
    assert json.loads(requests[0].content)["events"][0]["correlation_id"] == "checkout-123"
    assert requests[0].url.path == "/v2/events"


def test_note_idempotency_header_and_issue_assignment() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(201, json={"id": "note-1", "body": "checked"}, request=request)
        return httpx.Response(
            200,
            json={
                "id": "issue-1",
                "status": "open",
                "category": "missing_event",
                "severity": "medium",
                "message": "missing evidence",
                "assigned_to": None,
                "opened_at": "2026-01-01T00:00:00Z",
            },
            request=request,
        )

    with Reconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        client.issues.add_issue_note(
            "issue-1", AddNoteRequest(body="checked"), idempotency_key="note-1"
        )
        client.issues.update_issue("issue-1", PatchIssueRequest(assigned_to=None))

    assert requests[0].headers["Idempotency-Key"] == "note-1"
    assert requests[1].method == "PATCH"


def test_errors_are_typed_and_safe() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429,
            json={"title": "Too Many Requests", "code": "rate_limited", "message": "slow down"},
            headers={"X-Request-ID": "error-id"},
            request=request,
        )

    with Reconify(
        "rk_secret",
        base_url="http://api.test",
        retry=RetryConfig(max_retries=0),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        with pytest.raises(ReconifyRateLimitError) as caught:
            client.events.list_events()

    assert caught.value.code == "rate_limited"
    assert caught.value.request_id == "error-id"
    assert "rk_secret" not in str(caught.value)


@pytest.mark.parametrize(
    ("status", "error_type"),
    [
        (400, ReconifyRequestError),
        (401, ReconifyAuthenticationError),
        (403, ReconifyPermissionError),
        (404, ReconifyNotFoundError),
        (409, ReconifyConflictError),
        (429, ReconifyRateLimitError),
        (503, ReconifyServiceUnavailableError),
    ],
)
def test_public_error_statuses_are_typed(
    status: int, error_type: type[Exception]
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status,
            json={"code": "test_error", "message": "request rejected"},
            headers={"X-Request-ID": "status-id"},
            request=request,
        )

    with Reconify(
        "rk_test",
        base_url="http://api.test",
        retry=RetryConfig(max_retries=0),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        with pytest.raises(error_type) as caught:
            client.events.list_events()

    assert caught.value.status_code == status
    assert caught.value.request_id == "status-id"


def test_after_takes_precedence_over_offset() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"events": [], "limit": 10}, request=request)

    with Reconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        client.events.list_events(after="opaque", offset=100)

    assert requests[0].url.params == httpx.QueryParams("after=opaque")
