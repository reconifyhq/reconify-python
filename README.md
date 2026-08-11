# Reconify Python SDK

Typed synchronous and asynchronous clients for the public Reconify v1 API.

## Installation and quickstart

```sh
pip install reconify-python
```

```python
from reconify import Reconify

with Reconify(api_key="rk_...") as client:
    events = client.events.list_events(limit=25)
    for event in events.events:
        print(event.id, event.status)
```

The API key may also come from `RECONIFY_API_KEY`. The default endpoint is
`https://api.reconifyhq.com/v1`. `RECONIFY_API_URL` or `base_url` can select a
staging or self-hosted endpoint, and URLs with or without `/v1` are accepted.

## Public resources

The client exposes metadata, events, ingestion, issues, and organization. The
current public contract contains exactly 13 operations. Python methods use
`snake_case` names and typed Pydantic v2 models from `reconify.models`.

Sync and async clients provide cursor iterators:

```python
from reconify import AsyncReconify

async with AsyncReconify() as client:
    async for event in client.iter_events(limit=100):
        print(event.id)
```

Every operation supports `raw=True` for `RawResponse` and per-request timeout
through the `timeout` keyword. API errors expose status, detail, code,
validation details, response headers, and request ID without including keys or
request bodies. Safe methods retry bounded `429`, `503`, and transport failures
by default; unsafe retries require `RetryConfig(retry_unsafe_methods=True)`.

## Contract synchronization

```sh
python scripts/fetch_contract.py
python scripts/fetch_contract.py --latest
pytest -q tests/test_openapi_coverage.py
```

The default source is the public manifest at
<https://docs.reconifyhq.com/openapi/manifest.json>. For local SaaS changes,
set `RECONIFY_OPENAPI_SPEC` to an explicit OpenAPI JSON file. The SDK never
depends on another checkout or an absolute workspace path.

## Migration to 1.0.0

Version `1.0.0` targets the current monitoring and issue-investigation API. The
former ledger, wallet, setup, search, alert, and reconciliation methods are
removed because they are not part of the public contract. See
[UPGRADING.md](UPGRADING.md).

## Build and release

```sh
ruff check .
mypy src
pytest -q
python -m build
```

The release workflow publishes the built wheel to PyPI after a GitHub release.
Additive contract changes require a minor SDK release; SDK fixes require a
patch release; breaking public API changes require a new API version and SDK
major release.
