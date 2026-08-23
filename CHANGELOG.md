# Changelog

## 2.1.0

- Added optional `correlation_id` support to the typed monitoring event request
  model and ingestion serialization.

## 1.0.0

- Rebuilt the client for the current 13-operation public monitoring API.
- Added metadata, organization, issue notes, and issue-linked event resources.
- Removed the obsolete ledger, wallet, setup, search, alert, and reconciliation
  surface.
- Added pinned public OpenAPI synchronization and contract coverage checks.

## 0.1.0

- Initial typed Reconify Python SDK.
- Added sync and async clients for the retained 50-operation API surface.
- Excluded deep reconciliation adjustment, evidence, lifecycle, report-item,
  and signoff operations.
