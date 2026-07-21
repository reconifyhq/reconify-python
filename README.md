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

Every list operation also has a natural iterator on the client, for example
`client.iter_reconciliations(limit=100)` or
`client.iter_wallet_transactions(after="cursor")`. The async equivalent is
an async iterator. Iterators forward query parameters using keyword arguments,
so they never expose transport details.

## Errors and retries

HTTP failures raise typed `ReconifyError` subclasses. Every HTTP error exposes
`status_code`, `detail`, `code`, validation details, response headers, and the
response `request_id` without including credentials or request bodies.

429, 503, and transient HTTP transport failures such as timeouts are retried
for safe methods with bounded exponential backoff and jitter. Mutating methods
are not retried unless `RetryConfig(retry_unsafe_methods=True)` is supplied.
Transaction ingestion retries must reuse each row's `idempotencyKey`.

The client default timeout is 30 seconds. Individual operations can override
it with `timeout=...`, including an `httpx.Timeout` object. Async operations
also support normal `asyncio` cancellation, which is the Python equivalent of
context cancellation in other SDKs.

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

## API reference

The public operation methods are grouped by API module. Request bodies use the
typed Pydantic models exported from `reconify.models`; list query parameters use
the OpenAPI names in snake_case. Every operation accepts `raw=True` and a
per-request `timeout` override.

| Module | Methods |
| --- | --- |
| Alerts | `list_alert_rules`, `put_alert_rule` |
| Events | `list_events`, `get_event`, `reveal_event_field` |
| Ingestion | `ingest_integrity_events`, `ingest_integrity_test_events` |
| Issues | `list_issues`, `get_issue_summary`, `get_issue`, `update_issue`, `list_issue_deliveries`, `retry_issue_delivery`, `add_issue_note`, `resolve_issue` |
| Ledger | `list_ledger_sources`, `create_ledger_source`, `delete_ledger_source`, `get_ledger_source`, `update_ledger_source`, `list_source_periods`, `list_transactions`, `ingest_transactions` |
| Reconciliations | `list_integrity_sources_for_reconciliation`, `list_reconciliation_schedules`, `create_reconciliation_schedule`, `delete_reconciliation_schedule`, `get_reconciliation_schedule`, `update_reconciliation_schedule`, `list_reconciliations`, `create_reconciliation`, `get_reconciliation` |
| Search | `search_integrity_resources` |
| Setup | `list_setup_integrations`, `get_setup_integration`, `list_setup_sources`, `create_setup_source`, `get_setup_source`, `update_setup_source`, `disable_setup_source`, `create_test_session`, `get_test_session`, `get_test_session_result`, `retry_test_session`, `submit_test_session_events` |
| Transactions | `list_wallet_transactions`, `get_wallet_transaction` |
| Wallets | `list_wallets`, `get_wallet`, `get_wallet_balance` |

## Build and deploy

Build the distributable artifacts locally or in CI:

```bash
python -m pip install build
python -m build
```

The resulting wheel and source archive in `dist/` are ready for publication to
an internal or public Python package registry. CI builds both artifacts after
running lint, type checking, and tests.
