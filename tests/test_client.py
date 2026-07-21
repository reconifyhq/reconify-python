from __future__ import annotations

import json

import httpx
import pytest

from reconify import Reconify
from reconify.errors import ReconifyRateLimitError
from reconify.models import AlertRuleRequest, IngestEventsInputBody, IngestRow, SourceOutputBody
from reconify.transport import RetryConfig


def test_base_url_and_request_contract() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "source": {
                    "id": "source-1",
                    "orgId": "org-1",
                    "name": "Books",
                    "schemaMapping": {},
                    "createdAt": "2026-01-01T00:00:00Z",
                    "updatedAt": "2026-01-01T00:00:00Z",
                }
            },
            headers={"X-Request-ID": "response-id"},
            request=request,
        )

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport)
    with Reconify(
        "rk_test",
        base_url="http://localhost:3002/v1/",
        request_id="caller-id",
        http_client=http_client,
    ) as client:
        result = client.ledger.get_ledger_source("source id")

    assert isinstance(result, SourceOutputBody)
    assert requests[0].method == "GET"
    assert str(requests[0].url) == "http://localhost:3002/v1/ledger/sources/source%20id"
    assert requests[0].headers["Authorization"] == "Bearer rk_test"
    assert requests[0].headers["X-Request-ID"] == "caller-id"


def test_base_url_can_come_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RECONIFY_API_URL", "http://api.test/v1/")
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"events": [], "limit": 1}, request=request)

    with Reconify(
        "rk_test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        client.events.list_events()

    assert str(requests[0].url) == "http://api.test/v1/events"


def test_json_aliases_and_raw_response() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200, content=b'{"status":"ok"}', headers={"X-Request-ID": "r"}, request=request
        )

    with Reconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    ) as client:
        response = client.alerts.put_alert_rule(
            AlertRuleRequest(
                breachEnabled=True,
                controlId="control-1",
                dedupWindowSeconds=60,
                destinations={},
                resolutionEnabled=True,
                severityMin="low",
            ),
            raw=True,
        )

    assert response.status_code == 200
    assert response.request_id == "r"
    assert json.loads(response.body) == {"status": "ok"}
    assert requests[0].headers["Content-Type"] == "application/json"


def test_204_returns_none() -> None:
    with Reconify(
        "rk_test",
        base_url="http://api.test",
        http_client=httpx.Client(
            transport=httpx.MockTransport(lambda request: httpx.Response(204, request=request))
        ),
    ) as client:
        assert client.ledger.delete_ledger_source("source-1") is None


def test_errors_are_typed_and_safe() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429,
            json={
                "title": "Too Many Requests",
                "errors": [{"location": "$code", "message": "rate_limited"}],
            },
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


def test_models_preserve_aliases_and_tolerate_new_enum_values() -> None:
    row = IngestRow(
        idempotencyKey="row-1",
        date="2026-01-01",
        amountMinor=100,
        currency="USD",
        direction="future_direction",
    )
    assert row.idempotency_key == "row-1"
    assert row.direction.value == "future_direction"
    assert row.model_dump(by_alias=True)["idempotencyKey"] == "row-1"


def test_documented_batch_limits_are_validated() -> None:
    with pytest.raises(ValueError):
        IngestEventsInputBody(events=[])

    with pytest.raises(ValueError):
        IngestRow(
            idempotencyKey="row-1",
            date="2026-01-01",
            amountMinor=100,
            currency="USD",
            direction="debit",
            unexpected=True,
        )
