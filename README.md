# Reconify Python SDK

Typed synchronous and asynchronous clients for the Reconify Public API.

## Installation

```bash
pip install reconify
```

## Quickstart

```python
from reconify import Reconify

with Reconify(api_key="rk_...") as client:
    sources = client.ledger.list_ledger_sources(limit=25)
    for source in sources.sources or []:
        print(source.id, source.name)
```

The key may also be supplied through `RECONIFY_API_KEY`. The default endpoint is
`https://api.reconifyhq.com/v1`; pass `base_url="https://staging.example/v1"`
for staging or self-hosted deployments. `/v1` is added when it is absent.

## Async usage and pagination

```python
from reconify import AsyncReconify

async with AsyncReconify() as client:
    async for event in client.iter_events(limit=100):
        print(event.id)
```

Cursor and offset iterators preserve opaque cursors and the server's page size.
When an endpoint accepts both cursor and offset pagination, `after` takes
precedence.

## Errors and retries

HTTP failures raise typed `ReconifyError` subclasses. Every HTTP error exposes
`status_code`, `detail`, `code`, validation details, response headers, and the
response `request_id` without including credentials or request bodies.

429 and 503 responses are retried for safe methods with bounded exponential
backoff and jitter. Mutating methods are not retried unless
`RetryConfig(retry_unsafe_methods=True)` is supplied. Transaction ingestion
retries must reuse each row's `idempotencyKey`.

Use `raw=True` on any operation to receive status, headers, request ID, and raw
body through `RawResponse`.

## Test-session and ingestion headers

Integrity ingestion and test-session submission accept
`integrity_test_session=...`, which is sent as `X-Integrity-Test-Session`.
Integrity batches support 1–500 events and ledger transaction batches support
1–5000 transactions; the SDK does not truncate caller input.

The SDK intentionally excludes reconciliation adjustment, evidence, lifecycle,
report-item, and signoff operations. The retained reconciliation surface is
integrity sources, reconciliation list/create/get, and all schedule operations.

## Build and deploy

Build the distributable artifacts locally or in CI:

```bash
python -m pip install build
python -m build
```

The resulting wheel and source archive in `dist/` are ready for publication to
an internal or public Python package registry. CI builds both artifacts after
running lint, type checking, and tests.
