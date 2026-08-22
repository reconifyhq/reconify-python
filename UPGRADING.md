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
