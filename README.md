# Reconify Python SDK

Typed synchronous and asynchronous clients for sending events to the Reconify
Public API.

## Installation

```bash
pip install reconify-python
```

## Quickstart: send an integrity event

```python
from datetime import datetime, timezone

from reconify import Reconify
from reconify.models import IngestEventsInputBody, PublicEvent

event = PublicEvent(
    source_id="source_123",
    source_event_id="checkout-evt-123",
    event_type="payment.succeeded",
    occurred_at=datetime.now(timezone.utc),
    amount_minor=1250,
    currency="USD",
    wallet_id="wallet_123",
)

with Reconify(api_key="rk_...") as client:
    result = client.ingestion.ingest_integrity_events(
        IngestEventsInputBody(events=[event])
    )
    print(result.accepted, result.rejected)
```

The key may also be supplied through `RECONIFY_API_KEY`. The default endpoint
is `https://api.reconifyhq.com/v1`; pass
`base_url="https://staging.example/v1"` for staging or self-hosted
deployments. `/v1` is added when it is absent.

## Sending integrity events

The SDK has two direct integrity-event endpoints:

| Purpose | Method |
| --- | --- |
| Send production integrity events | `client.ingestion.ingest_integrity_events(...)` |
| Send test-session integrity events | `client.ingestion.ingest_integrity_test_events(...)` |

Both accept an `IngestEventsInputBody` containing typed `PublicEvent` models.
Python model fields use `snake_case`; the SDK serializes them to the API’s
wire format.

### Send a batch and inspect partial results

```python
from datetime import datetime, timezone

from reconify import Reconify
from reconify.models import IngestEventsInputBody, PublicEvent

batch = IngestEventsInputBody(
    events=[
        PublicEvent(
            source_id="source_123",
            source_event_id="payment-evt-123",
            event_type="payment.succeeded",
            occurred_at=datetime(2026, 1, 31, 12, 0, tzinfo=timezone.utc),
            amount_minor=1250,
            currency="USD",
            wallet_id="wallet_123",
            external_reference="order-123",
            metadata={"channel": "web"},
        ),
        PublicEvent(
            source_id="source_123",
            source_event_id="refund-evt-456",
            event_type="payment.refunded",
            occurred_at=datetime(2026, 1, 31, 12, 5, tzinfo=timezone.utc),
            amount_minor=-250,
            currency="USD",
            wallet_id="wallet_123",
            external_reference="order-123",
        ),
    ]
)

with Reconify() as client:
    result = client.ingestion.ingest_integrity_events(batch)

    for accepted in result.accepted or []:
        print("accepted", accepted.index, accepted.source_event_id)
    for rejected in result.rejected or []:
        print("rejected", rejected.index, rejected.code, rejected.reason)
```

`source_event_id` identifies the source event. Keep it stable when retrying the
same event. The API returns accepted and rejected rows independently, so a
batch can contain both successful and rejected events.

### Send test-session events

Test-session events use the same event models. Pass the test-session token as
`integrity_test_session`; the SDK sends it as
`X-Integrity-Test-Session`.

```python
with Reconify() as client:
    result = client.ingestion.ingest_integrity_test_events(
        batch,
        integrity_test_session="test-session-token",
    )
    print(result.accepted, result.rejected)
```

### Submit events to a setup test session

After a test session has been created, submit its events with the setup
endpoint. This is also a sending operation and accepts the same `PublicEvent`
models.

```python
from reconify import Reconify
from reconify.models import SetupSubmitSessionInputBody

with Reconify() as client:
    result = client.setup.submit_test_session_events(
        "session_123",
        SetupSubmitSessionInputBody(events=batch.events),
        integrity_test_session="test-session-token",
    )
    print(result.accepted, result.rejected)
```

## Batch limits and validation

- Integrity event batches contain 1–500 events.
- Integrity event requests must not exceed 5 MiB.
- Invalid model fields and batch sizes are rejected before an HTTP request is
  sent.
- Event payloads can include `amount_minor`, `currency`, `wallet_id`,
  `external_reference`, `provider_reference`, `operation_id`, and `metadata`.

## Async sending

`AsyncReconify` exposes the same sending operations. Use `async with` to close
the underlying HTTP client automatically.

```python
import asyncio

from reconify import AsyncReconify


async def send_events() -> None:
    async with AsyncReconify() as client:
        result = await client.ingestion.ingest_integrity_events(batch)
        print(result.accepted, result.rejected)


asyncio.run(send_events())
```

Async operations support normal `asyncio` cancellation.

## Retries, timeouts, and failures

Mutating requests are not retried by default. If a sending workflow can safely
replay the same stable event IDs, opt into unsafe retries explicitly.

```python
from reconify import Reconify
from reconify.errors import ReconifyRequestError
from reconify.transport import RetryConfig

with Reconify(
    request_id="trace-123",
    retry=RetryConfig(max_retries=2, retry_unsafe_methods=True),
) as client:
    try:
        result = client.ingestion.ingest_integrity_events(batch, timeout=10)
    except ReconifyRequestError as exc:
        print(exc.status_code, exc.detail, exc.request_id)
```

HTTP failures raise typed `ReconifyError` subclasses. Each error exposes the
status code, detail, error code, validation details, response headers, and
request ID without including credentials or request bodies.

Use `raw=True` when the sending workflow needs the status, headers, request ID,
and unparsed response body:

```python
with Reconify() as client:
    response = client.ingestion.ingest_integrity_events(batch, raw=True)
    print(response.status_code, response.request_id)
    print(response.json())
```

The client default timeout is 30 seconds. Individual sending operations can
override it with `timeout=...`, including an `httpx.Timeout` object.

## Build and deploy

Build the distributable artifacts locally or in CI:

```bash
python -m pip install build
python -m build
```

The resulting wheel and source archive in `dist/` are ready for publication to
an internal or public Python package registry. CI builds both artifacts after
running lint, type checking, and tests.
