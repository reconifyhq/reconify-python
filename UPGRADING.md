# Upgrading to 2.0.0

The 2.0.0 client targets the public Reconify v2 contract at `/v2`.
Generated operation IDs now use stable `resource_action` identifiers. The
Python resource methods keep their existing snake_case names.

Use these resources:

- metadata: API information and health
- events: event listing, lookup, and issue-linked evidence
- ingestion: monitoring event batches
- issues: issue listing, lookup, assignment, notes, and linked data
- organization: organization and member reads

Python models use snake_case fields and preserve unknown enum values through
tolerant string enums. Existing v1 clients can continue using `/v1`; v2
clients must use the v2 artifact and endpoint.

## Upgrading to 2.1.0

The 2.1.0 client adds the optional `correlation_id` field to
`MonitoringEvent`. Use it when the same transaction spans services that report
different references:

```python
MonitoringEvent(
    flow="payment_to_wallet",
    type="payment.succeeded",
    reference="order-123",
    entity_id="wallet-123",
    correlation_id="checkout-123",
)
```

The value is sent as event metadata and does not change operation grouping or
evaluation behavior.

## Upgrading to 2.2.0

The 2.2.0 client follows public API contract 2.3.0. Monitoring ingestion now
accepts a single `MonitoringEvent`, a list of events, or the existing
`MonitoringBatchRequest` wrapper. Settlement flows and event types support
financial breakdowns, allocations, causation IDs, and revision IDs.

On-chain evidence enrichment can be queued for an accepted event:

```python
client.onchain.register_onchain_source(
    OnchainSourceRequest(
        flow="provider_to_settlement_account",
        operation_reference="settlement-123",
        source_event_id="evt_01J3Y0M8VJQ5W1R3E4J4K7N8P9",
        kind="transaction",
        locator=OnchainSourceLocator(
            network="ethereum-mainnet",
            transaction_reference="0x...",
        ),
    ),
    idempotency_key="source-settlement-123",
)
```
