# Upgrading to 1.0.0

The 1.0.0 client is rebuilt against the current public Reconify v1 contract.
It removes methods that described private or retired ledger, wallet, setup,
search, alert, and reconciliation routes.

Use these resources:

- metadata: API information and health
- events: event listing, lookup, and issue-linked evidence
- ingestion: monitoring event batches
- issues: issue listing, lookup, assignment, notes, and linked data
- organization: organization and member reads

Python models use snake_case fields and preserve unknown enum values through
tolerant string enums. Regenerate or refresh the models after downloading a
new public contract version.
