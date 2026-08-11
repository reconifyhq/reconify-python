# Reconify Python SDK agent guide

This repository publishes reconify-python, the typed synchronous and
asynchronous client for the public Reconify /v1 API.

## Contract authority

The SaaS Go API owns the contract. Fetch the pinned public artifact with
python scripts/fetch_contract.py, or update to the manifest version with
python scripts/fetch_contract.py --latest.

For local SaaS work, set RECONIFY_OPENAPI_SPEC to an explicit OpenAPI JSON
file. Do not use sibling repositories or absolute workspace paths.

The resource and transport layers are handwritten for Python ergonomics.
tests/test_openapi_coverage.py is the contract boundary and must remain
spec-driven. Keep Pydantic models aligned with the downloaded schemas.

## Supported surface

The SDK exposes metadata, events, ingestion, issues, and organization
resources. Internal /business/v1 routes and the former ledger, wallet, setup,
search, alert, and reconciliation surface are not public SDK APIs.

## Verification

Run ruff check ., mypy src, pytest -q, and python -m build before releasing.
Keep credentials out of errors and logs, preserve request IDs, and update
examples and migration notes when the public contract changes.
