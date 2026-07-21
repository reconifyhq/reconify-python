"""Complete Pydantic v2 model surface derived from the Reconify OpenAPI schemas."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TolerantStrEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: object) -> TolerantStrEnum | None:
        if isinstance(value, str):
            member = str.__new__(cls, value)
            member._name_ = f"UNKNOWN_{value.upper().replace('-', '_')}"
            member._value_ = value
            cls._value2member_map_[value] = member
            return member
        return None


class ResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True, validate_assignment=True)


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)


class AdjustmentRequestBodyAdjustmentType(TolerantStrEnum):
    FEE = "fee"
    REVERSAL = "reversal"
    RECLASSIFICATION = "reclassification"
    MANUAL_CORRECTION = "manual_correction"
    WRITE_OFF = "write_off"
    SPLIT_ALLOCATION = "split_allocation"


class EventWindowBasis(TolerantStrEnum):
    RECEIVED_AT = "received_at"
    OCCURRED_AT = "occurred_at"


class IngestRowDirection(TolerantStrEnum):
    DEBIT = "debit"
    CREDIT = "credit"


class IngestRowStatus(TolerantStrEnum):
    PENDING = "pending"
    POSTED = "posted"
    FAILED = "failed"
    REVERSED = "reversed"
    VOID = "void"


class PublicAdjustmentStatus(TolerantStrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    APPLIED = "applied"
    REVERSED = "reversed"
    REJECTED = "rejected"


class PublicSignoffRole(TolerantStrEnum):
    PREPARED_BY = "prepared_by"
    REVIEWED_BY = "reviewed_by"
    APPROVED_BY = "approved_by"


class ReconciliationScheduleFrequency(TolerantStrEnum):
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ReconciliationScheduleStatus(TolerantStrEnum):
    ACTIVE = "active"
    PAUSED = "paused"


class ReconciliationScheduleWindowBasis(TolerantStrEnum):
    RECEIVED_AT = "received_at"
    OCCURRED_AT = "occurred_at"


class ScheduleRequestBodyFrequency(TolerantStrEnum):
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ScheduleRequestBodyStatus(TolerantStrEnum):
    ACTIVE = "active"
    PAUSED = "paused"


class ScheduleRequestBodyWindowBasis(TolerantStrEnum):
    RECEIVED_AT = "received_at"
    OCCURRED_AT = "occurred_at"


class ScheduleUpdateRequestBodyFrequency(TolerantStrEnum):
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ScheduleUpdateRequestBodyStatus(TolerantStrEnum):
    ACTIVE = "active"
    PAUSED = "paused"


class ScheduleUpdateRequestBodyWindowBasis(TolerantStrEnum):
    RECEIVED_AT = "received_at"
    OCCURRED_AT = "occurred_at"


class SourceRefRole(TolerantStrEnum):
    LEFT = "left"
    RIGHT = "right"


class TransactionDetailResourceStatus(TolerantStrEnum):
    PENDING = "pending"
    POSTED = "posted"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


class WalletTransactionStatus(TolerantStrEnum):
    PENDING = "pending"
    POSTED = "posted"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


class AcceptedResult(ResponseModel):
    index: int = Field(alias="index")
    source_event_id: str = Field(alias="sourceEventId")


class Activity(ResponseModel):
    action: str = Field(alias="action")
    actor_user_id: str | None = Field(default=None, alias="actorUserId", exclude=False)
    created_at: datetime = Field(alias="createdAt")
    event_id: str | None = Field(default=None, alias="eventId", exclude=False)
    finding_id: str | None = Field(default=None, alias="findingId", exclude=False)
    id: str = Field(alias="id")
    metadata: dict[str, Any] = Field(alias="metadata")
    operation_id: str | None = Field(default=None, alias="operationId", exclude=False)


class AdjustmentOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    adjustment: PublicAdjustment = Field(alias="adjustment")


class AdjustmentRequestBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    adjustment_type: AdjustmentRequestBodyAdjustmentType = Field(alias="adjustmentType")
    amount_minor: int | None = Field(default=None, alias="amountMinor", exclude=False)
    currency: str | None = Field(default=None, alias="currency", exclude=False)
    note: str | None = Field(default=None, alias="note", exclude=False)
    resolution_reason: str | None = Field(default=None, alias="resolutionReason", exclude=False)
    result_item_id: int | None = Field(default=None, alias="resultItemId", exclude=False)


class AlertLink(ResponseModel):
    channel: str = Field(alias="channel")
    created_at: datetime = Field(alias="createdAt")
    finding_id: str = Field(alias="findingId")
    id: str = Field(alias="id")
    sent_at: datetime | None = Field(default=None, alias="sentAt", exclude=False)
    status: str = Field(alias="status")
    transition: str = Field(alias="transition")


class AlertRule(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    breach_enabled: bool = Field(alias="breachEnabled")
    channels: list[str] | None = Field(alias="channels")
    control_id: str = Field(alias="controlId")
    dedup_window_seconds: int = Field(alias="dedupWindowSeconds")
    destinations: dict[str, Any] = Field(alias="destinations")
    resolution_enabled: bool = Field(alias="resolutionEnabled")
    severity_min: str = Field(alias="severityMin")
    suppressed_until: datetime | None = Field(default=None, alias="suppressedUntil", exclude=False)
    suppression_reason: str | None = Field(default=None, alias="suppressionReason", exclude=False)


class AlertRulesOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    rules: list[AlertRule] | None = Field(alias="rules")


class BatchResponse(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    accepted: list[AcceptedResult] | None = Field(alias="accepted")
    rejected: list[RejectedResult] | None = Field(alias="rejected")


class CreateReconciliationInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    event_config: EventReconciliationConfig | None = Field(
        default=None, alias="event_config", exclude=False
    )
    ledger_config: LedgerConfig | None = Field(default=None, alias="ledger_config", exclude=False)
    name: str | None = Field(default=None, alias="name", exclude=False)


class CreateSessionRequest(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    control_id: str = Field(alias="controlId")


class CreateSourceInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    name: str = Field(alias="name")
    schema_mapping: SchemaMap | None = Field(default=None, alias="schemaMapping", exclude=False)


class CreateSourceRequest(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    config: dict[str, Any] | None = Field(default=None, alias="config", exclude=False)
    name: str = Field(alias="name")
    source_type: str = Field(alias="sourceType")


class DeliveriesOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    deliveries: list[Delivery] | None = Field(alias="deliveries")


class Delivery(ResponseModel):
    attempt_count: int = Field(alias="attemptCount")
    channel: str = Field(alias="channel")
    destination: str = Field(alias="destination")
    id: str = Field(alias="id")
    last_error_code: str | None = Field(default=None, alias="lastErrorCode", exclude=False)
    next_attempt_at: datetime = Field(alias="nextAttemptAt")
    sent_at: datetime | None = Field(default=None, alias="sentAt", exclude=False)
    status: str = Field(alias="status")
    transition: str = Field(alias="transition")


class ErrorDetail(ResponseModel):
    location: str | None = Field(default=None, alias="location", exclude=False)
    message: str | None = Field(default=None, alias="message", exclude=False)
    value: Any | None = Field(default=None, alias="value", exclude=False)


class ErrorModel(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    detail: str | None = Field(default=None, alias="detail", exclude=False)
    errors: list[ErrorDetail] | None = Field(default=None, alias="errors", exclude=False)
    instance: str | None = Field(default=None, alias="instance", exclude=False)
    status: int | None = Field(default=None, alias="status", exclude=False)
    title: str | None = Field(default=None, alias="title", exclude=False)
    type: str | None = Field(default=None, alias="type", exclude=False)


class Event(ResponseModel):
    amount_minor: int = Field(alias="amountMinor")
    applied: bool = Field(alias="applied")
    balance_minor: int | None = Field(default=None, alias="balanceMinor", exclude=False)
    canonical_hash: str = Field(alias="canonicalHash")
    correlation_namespace: str | None = Field(
        default=None, alias="correlationNamespace", exclude=False
    )
    currency: str = Field(alias="currency")
    entity_reference: str | None = Field(default=None, alias="entityReference", exclude=False)
    event_schema_version: int = Field(alias="eventSchemaVersion")
    event_type: str = Field(alias="eventType")
    external_reference: str | None = Field(default=None, alias="externalReference", exclude=False)
    finding_id: str | None = Field(default=None, alias="findingId", exclude=False)
    id: str = Field(alias="id")
    occurred_at: datetime = Field(alias="occurredAt")
    operation_id: str | None = Field(default=None, alias="operationId", exclude=False)
    operation_type: str | None = Field(default=None, alias="operationType", exclude=False)
    processing_status: str = Field(alias="processingStatus")
    provider_reference: str | None = Field(default=None, alias="providerReference", exclude=False)
    received_at: datetime = Field(alias="receivedAt")
    source_event_id: str = Field(alias="sourceEventId")
    source_id: str = Field(alias="sourceId")
    supersedes_event_id: str | None = Field(default=None, alias="supersedesEventId", exclude=False)
    wallet_id: str | None = Field(default=None, alias="walletId", exclude=False)


class EventDetail(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    event: Event = Field(alias="event")
    metadata: dict[str, Any] = Field(alias="metadata")
    payload: dict[str, Any] = Field(alias="payload")
    timeline: list[EventTimelineItem] | None = Field(alias="timeline")


class EventPage(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    events: list[Event] | None = Field(alias="events")
    limit: int = Field(alias="limit")
    next_cursor: str | None = Field(default=None, alias="nextCursor", exclude=False)


class EventReconciliationConfig(ResponseModel):
    anchor_source_id: str = Field(alias="anchor_source_id")
    correlation_namespace: str | None = Field(
        default=None, alias="correlation_namespace", exclude=False
    )
    source_ids: list[str] | None = Field(alias="source_ids")
    window: EventWindow = Field(alias="window")


class EventRevealOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    field: str = Field(alias="field")
    value: Any = Field(alias="value")


class EventTimelineItem(ResponseModel):
    action: str = Field(alias="action")
    created_at: datetime = Field(alias="createdAt")
    kind: str = Field(alias="kind")


class EventWindow(ResponseModel):
    basis: EventWindowBasis = Field(alias="basis")
    end: str = Field(alias="end")
    start: str = Field(alias="start")


class EvidenceOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    evidence: PublicEvidence = Field(alias="evidence")


class EvidenceRequestBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    checksum_sha256: str | None = Field(default=None, alias="checksumSha256", exclude=False)
    entity_id: str = Field(alias="entityId")
    entity_type: str = Field(alias="entityType")
    evidence_type: str = Field(alias="evidenceType")
    metadata: dict[str, Any] | None = Field(default=None, alias="metadata", exclude=False)
    storage_path: str | None = Field(default=None, alias="storagePath", exclude=False)


class IngestError(ResponseModel):
    idempotency_key: str | None = Field(default=None, alias="idempotencyKey", exclude=False)
    index: int = Field(alias="index")
    message: str = Field(alias="message")


class IngestEventsInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    events: list[PublicEvent] | None = Field(alias="events", min_length=1, max_length=500)


class IngestRow(RequestModel):
    amount_minor: int = Field(alias="amountMinor")
    currency: str = Field(alias="currency")
    date: str = Field(alias="date")
    direction: IngestRowDirection = Field(alias="direction")
    idempotency_key: str = Field(alias="idempotencyKey")
    metadata: Any | None = Field(default=None, alias="metadata", exclude=False)
    name: str | None = Field(default=None, alias="name", exclude=False)
    period_key: str | None = Field(default=None, alias="periodKey", exclude=False)
    raw: Any | None = Field(default=None, alias="raw", exclude=False)
    reference: str | None = Field(default=None, alias="reference", exclude=False)
    status: IngestRowStatus | None = Field(default=None, alias="status", exclude=False)
    transaction_type: str | None = Field(default=None, alias="transactionType", exclude=False)
    value_date: str | None = Field(default=None, alias="valueDate", exclude=False)


class IngestTransactionsInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    transactions: list[IngestRow] | None = Field(
        alias="transactions", min_length=1, max_length=5000
    )


class IngestTransactionsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    duplicates: int = Field(alias="duplicates")
    errors: list[IngestError] | None = Field(default=None, alias="errors", exclude=False)
    ingested: int = Field(alias="ingested")


class IntegritySource(ResponseModel):
    id: str = Field(alias="id")
    name: str = Field(alias="name")
    source_type: str = Field(alias="sourceType")


class Issue(ResponseModel):
    affected_transaction_count: int | None = Field(
        default=None, alias="affectedTransactionCount", exclude=False
    )
    affected_wallet_count: int | None = Field(
        default=None, alias="affectedWalletCount", exclude=False
    )
    assigned_to: str | None = Field(default=None, alias="assignedTo", exclude=False)
    control_id: str | None = Field(default=None, alias="controlId", exclude=False)
    currency: str | None = Field(default=None, alias="currency", exclude=False)
    event_id: str | None = Field(default=None, alias="eventId", exclude=False)
    exposure_minor: int | None = Field(default=None, alias="exposureMinor", exclude=False)
    id: str = Field(alias="id")
    kind: str = Field(alias="kind")
    opened_at: datetime = Field(alias="openedAt")
    operation_id: str | None = Field(default=None, alias="operationId", exclude=False)
    reason: str = Field(alias="reason")
    resolved_at: datetime | None = Field(default=None, alias="resolvedAt", exclude=False)
    severity: str = Field(alias="severity")
    system_outcome: str | None = Field(default=None, alias="systemOutcome", exclude=False)
    workflow_status: str = Field(alias="workflowStatus")


class IssueCounts(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    acknowledged: int = Field(alias="acknowledged")
    failed_delivery: int = Field(alias="failedDelivery")
    investigating: int = Field(alias="investigating")
    open: int = Field(alias="open")
    resolved: int = Field(alias="resolved")


class IssueDetail(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    activity: list[Activity] | None = Field(alias="activity")
    deliveries: list[Delivery] | None = Field(alias="deliveries")
    issue: Issue = Field(alias="issue")
    notes: list[Note] | None = Field(alias="notes")


class IssuePage(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    issues: list[Issue] | None = Field(alias="issues")
    limit: int = Field(alias="limit")
    next_cursor: str | None = Field(default=None, alias="nextCursor", exclude=False)


class IssueUpdateInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    assigned_to: str | None = Field(default=None, alias="assignedTo", exclude=False)
    workflow_status: str | None = Field(default=None, alias="workflowStatus", exclude=False)


class LedgerConfig(ResponseModel):
    period_key: str = Field(alias="period_key")
    sources: list[SourceRef] | None = Field(alias="sources")


class ListAdjustmentsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    adjustments: list[PublicAdjustment] | None = Field(alias="adjustments")
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    total: int = Field(alias="total")


class ListEvidenceOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    evidence: list[PublicEvidence] | None = Field(alias="evidence")


class ListIntegritySourcesOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    sources: list[IntegritySource] | None = Field(alias="sources")


class ListPeriodsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    periods: list[PeriodHealth] | None = Field(alias="periods")


class ListReconciliationItemsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    category: str = Field(alias="category")
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    rows: list[PublicResultItem] | None = Field(alias="rows")
    total: int = Field(alias="total")


class ListReconciliationsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    reconciliations: list[Reconciliation] | None = Field(alias="reconciliations")
    total: int = Field(alias="total")


class ListSchedulesOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    schedules: list[ReconciliationSchedule] | None = Field(alias="schedules")
    total: int = Field(alias="total")


class ListSignoffsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    signoffs: list[PublicSignoff] | None = Field(alias="signoffs")


class ListSourcesOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    sources: list[Source] | None = Field(alias="sources")
    total: int = Field(alias="total")


class ListTransactionsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    next_cursor: str | None = Field(default=None, alias="nextCursor", exclude=False)
    offset: int = Field(alias="offset")
    total: int = Field(alias="total")
    transactions: list[Transaction] | None = Field(alias="transactions")


class Note(ResponseModel):
    author_user_id: str = Field(alias="authorUserId")
    body: str = Field(alias="body")
    created_at: datetime = Field(alias="createdAt")
    id: str = Field(alias="id")


class NoteInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    body: str = Field(alias="body")


class PeriodHealth(ResponseModel):
    currency: str = Field(alias="currency")
    has_run: bool = Field(alias="hasRun")
    period_key: str = Field(alias="periodKey")
    total_amount_minor: int = Field(alias="totalAmountMinor")
    tx_count: int = Field(alias="txCount")


class PublicAdjustment(ResponseModel):
    adjustment_type: str = Field(alias="adjustmentType")
    amount_minor: int | None = Field(default=None, alias="amountMinor", exclude=False)
    applied_at: datetime | None = Field(default=None, alias="appliedAt", exclude=False)
    approved_at: datetime | None = Field(default=None, alias="approvedAt", exclude=False)
    created_at: datetime = Field(alias="createdAt")
    created_by_email: str | None = Field(default=None, alias="createdByEmail", exclude=False)
    currency: str | None = Field(default=None, alias="currency", exclude=False)
    id: str = Field(alias="id")
    note: str = Field(alias="note")
    reconciliation_id: str = Field(alias="reconciliationId")
    rejected_at: datetime | None = Field(default=None, alias="rejectedAt", exclude=False)
    resolution_reason: str = Field(alias="resolutionReason")
    result_item_id: int | None = Field(default=None, alias="resultItemId", exclude=False)
    reversed_at: datetime | None = Field(default=None, alias="reversedAt", exclude=False)
    status: PublicAdjustmentStatus = Field(alias="status")


class PublicEvent(ResponseModel):
    amount_minor: int = Field(alias="amountMinor")
    balance_minor: int | None = Field(default=None, alias="balanceMinor", exclude=False)
    correlation_namespace: str | None = Field(
        default=None, alias="correlationNamespace", exclude=False
    )
    currency: str = Field(alias="currency")
    entity_reference: str | None = Field(default=None, alias="entityReference", exclude=False)
    event_schema_version: int | None = Field(
        default=None, alias="eventSchemaVersion", exclude=False
    )
    event_type: str = Field(alias="eventType")
    external_reference: str | None = Field(default=None, alias="externalReference", exclude=False)
    metadata: dict[str, Any] | None = Field(default=None, alias="metadata", exclude=False)
    occurred_at: datetime = Field(alias="occurredAt")
    operation_id: str | None = Field(default=None, alias="operationId", exclude=False)
    operation_type: str | None = Field(default=None, alias="operationType", exclude=False)
    provider_reference: str | None = Field(default=None, alias="providerReference", exclude=False)
    source_event_id: str = Field(alias="sourceEventId")
    source_id: str = Field(alias="sourceId")
    supersedes_source_event_id: str | None = Field(
        default=None, alias="supersedesSourceEventId", exclude=False
    )
    wallet_id: str | None = Field(default=None, alias="walletId", exclude=False)


class PublicEvidence(ResponseModel):
    created_at: datetime = Field(alias="createdAt")
    entity_id: str = Field(alias="entityId")
    entity_type: str = Field(alias="entityType")
    evidence_type: str = Field(alias="evidenceType")
    id: str = Field(alias="id")
    metadata: dict[str, Any] = Field(alias="metadata")
    reconciliation_id: str = Field(alias="reconciliationId")


class PublicResultItem(ResponseModel):
    amount_minor: int | None = Field(default=None, alias="amountMinor", exclude=False)
    assigned_to: str | None = Field(default=None, alias="assignedTo", exclude=False)
    category: str = Field(alias="category")
    currency: str | None = Field(default=None, alias="currency", exclude=False)
    exception_opened_at: str | None = Field(default=None, alias="exceptionOpenedAt", exclude=False)
    exception_status: str = Field(alias="exceptionStatus")
    id: int = Field(alias="id")
    is_escalated: bool = Field(alias="isEscalated")
    left_name: str | None = Field(default=None, alias="leftName", exclude=False)
    note: str | None = Field(default=None, alias="note", exclude=False)
    payload: dict[str, Any] = Field(alias="payload")
    reason_code: str | None = Field(default=None, alias="reasonCode", exclude=False)
    reference: str | None = Field(default=None, alias="reference", exclude=False)
    review_status: str = Field(alias="reviewStatus")
    right_name: str | None = Field(default=None, alias="rightName", exclude=False)
    side: str | None = Field(default=None, alias="side", exclude=False)
    type: str = Field(alias="type")


class PublicSignoff(ResponseModel):
    approval_note: str = Field(alias="approvalNote")
    id: str = Field(alias="id")
    reconciliation_id: str = Field(alias="reconciliationId")
    role: PublicSignoffRole = Field(alias="role")
    signed_at: datetime = Field(alias="signedAt")
    signed_with_exceptions: bool = Field(alias="signedWithExceptions")
    signer_name: str = Field(alias="signerName")
    signer_title: str = Field(alias="signerTitle")


class Reconciliation(ResponseModel):
    completed_at: datetime | None = Field(default=None, alias="completedAt", exclude=False)
    created_at: datetime = Field(alias="createdAt")
    current_stage: str = Field(alias="currentStage")
    id: str = Field(alias="id")
    last_error_message: str | None = Field(default=None, alias="lastErrorMessage", exclude=False)
    ledger_config: Any | None = Field(default=None, alias="ledgerConfig", exclude=False)
    name: str | None = Field(default=None, alias="name", exclude=False)
    org_id: str = Field(alias="orgId")
    progress_pct: float = Field(alias="progressPct")
    run_mode: str = Field(alias="runMode")
    started_at: datetime | None = Field(default=None, alias="startedAt", exclude=False)
    status: str = Field(alias="status")
    updated_at: datetime = Field(alias="updatedAt")


class ReconciliationLink(ResponseModel):
    category: str = Field(alias="category")
    exception_status: str = Field(alias="exceptionStatus")
    match_basis: str = Field(alias="matchBasis")
    reconciliation_id: str = Field(alias="reconciliationId")
    reconciliation_name: str | None = Field(default=None, alias="reconciliationName", exclude=False)
    reference: str = Field(alias="reference")
    result_item_id: int = Field(alias="resultItemId")


class ReconciliationOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    reconciliation: Reconciliation = Field(alias="reconciliation")


class ReconciliationSchedule(ResponseModel):
    anchor_source_id: str = Field(alias="anchorSourceId")
    correlation_namespace: str | None = Field(
        default=None, alias="correlationNamespace", exclude=False
    )
    created_at: datetime = Field(alias="createdAt")
    frequency: ReconciliationScheduleFrequency = Field(alias="frequency")
    id: str = Field(alias="id")
    last_run_id: str | None = Field(default=None, alias="lastRunId", exclude=False)
    next_run_at: datetime = Field(alias="nextRunAt")
    rolling_window_duration: str = Field(alias="rollingWindowDuration")
    source_ids: list[str] | None = Field(alias="sourceIds")
    status: ReconciliationScheduleStatus = Field(alias="status")
    updated_at: datetime = Field(alias="updatedAt")
    window_basis: ReconciliationScheduleWindowBasis = Field(alias="windowBasis")


class RejectedResult(ResponseModel):
    code: str = Field(alias="code")
    index: int = Field(alias="index")
    reason: str = Field(alias="reason")


class RelatedEvent(ResponseModel):
    amount_minor: int = Field(alias="amountMinor")
    currency: str = Field(alias="currency")
    entity_reference: str | None = Field(default=None, alias="entityReference", exclude=False)
    event_id: str = Field(alias="eventId")
    event_type: str = Field(alias="eventType")
    evidence_role: str = Field(alias="evidenceRole")
    external_reference: str | None = Field(default=None, alias="externalReference", exclude=False)
    occurred_at: datetime = Field(alias="occurredAt")
    provider_reference: str | None = Field(default=None, alias="providerReference", exclude=False)
    received_at: datetime = Field(alias="receivedAt")
    source_event_id: str = Field(alias="sourceEventId")
    source_id: str = Field(alias="sourceId")
    superseded_by_event_id: str | None = Field(
        default=None, alias="supersededByEventId", exclude=False
    )


class ResolveInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    evidence_attachment_id: str = Field(alias="evidenceAttachmentId")
    reason: str = Field(alias="reason")


class ScheduleOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    schedule: ReconciliationSchedule = Field(alias="schedule")


class ScheduleRequestBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    anchor_source_id: str = Field(alias="anchor_source_id")
    correlation_namespace: str | None = Field(
        default=None, alias="correlation_namespace", exclude=False
    )
    frequency: ScheduleRequestBodyFrequency = Field(alias="frequency")
    next_run_at: datetime | None = Field(default=None, alias="next_run_at", exclude=False)
    rolling_window_duration: str | None = Field(
        default=None, alias="rolling_window_duration", exclude=False
    )
    source_ids: list[str] | None = Field(alias="source_ids", min_length=2)
    status: ScheduleRequestBodyStatus | None = Field(default=None, alias="status", exclude=False)
    window_basis: ScheduleRequestBodyWindowBasis = Field(alias="window_basis")


class ScheduleUpdateRequestBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    anchor_source_id: str | None = Field(default=None, alias="anchor_source_id", exclude=False)
    correlation_namespace: str | None = Field(
        default=None, alias="correlation_namespace", exclude=False
    )
    frequency: ScheduleUpdateRequestBodyFrequency | None = Field(
        default=None, alias="frequency", exclude=False
    )
    next_run_at: datetime | None = Field(default=None, alias="next_run_at", exclude=False)
    rolling_window_duration: str | None = Field(
        default=None, alias="rolling_window_duration", exclude=False
    )
    source_ids: list[str] | None = Field(default=None, alias="source_ids", min_length=2)
    status: ScheduleUpdateRequestBodyStatus | None = Field(
        default=None, alias="status", exclude=False
    )
    window_basis: ScheduleUpdateRequestBodyWindowBasis | None = Field(
        default=None, alias="window_basis", exclude=False
    )


class SchemaMap(ResponseModel):
    amount_col: str | None = Field(default=None, alias="amountCol", exclude=False)
    currency_col: str | None = Field(default=None, alias="currencyCol", exclude=False)
    date_col: str | None = Field(default=None, alias="dateCol", exclude=False)
    date_layout: str | None = Field(default=None, alias="dateLayout", exclude=False)
    decimal: str | None = Field(default=None, alias="decimal", exclude=False)
    direction_col: str | None = Field(default=None, alias="directionCol", exclude=False)
    name_col: str | None = Field(default=None, alias="nameCol", exclude=False)
    ref_col: str | None = Field(default=None, alias="refCol", exclude=False)
    thousands: str | None = Field(default=None, alias="thousands", exclude=False)
    type_col: str | None = Field(default=None, alias="typeCol", exclude=False)


class SearchPage(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    results: list[SearchResult] | None = Field(alias="results")


class SearchResult(ResponseModel):
    id: str = Field(alias="id")
    kind: str = Field(alias="kind")
    occurred_at: datetime = Field(alias="occurredAt")
    status: str | None = Field(default=None, alias="status", exclude=False)
    subtitle: str | None = Field(default=None, alias="subtitle", exclude=False)
    title: str = Field(alias="title")


class SetupIntegration(ResponseModel):
    capabilities: list[str] | None = Field(default=None, alias="capabilities", exclude=False)
    created_at: datetime = Field(alias="createdAt")
    health: str = Field(alias="health")
    id: str = Field(alias="id")
    name: str = Field(alias="name")
    status: str = Field(alias="status")
    type: str = Field(alias="type")
    updated_at: datetime = Field(alias="updatedAt")


class SetupIntegrationOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    integration: SetupIntegration = Field(alias="integration")


class SetupIntegrationsOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    integrations: list[SetupIntegration] | None = Field(alias="integrations")


class SetupSessionDiff(ResponseModel):
    missing: list[str] | None = Field(alias="missing")
    unexpected: list[str] | None = Field(alias="unexpected")


class SetupSessionOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    test_session: SetupTestSession = Field(alias="testSession")


class SetupSource(ResponseModel):
    config: dict[str, Any] | None = Field(default=None, alias="config", exclude=False)
    created_at: datetime = Field(alias="createdAt")
    id: str = Field(alias="id")
    name: str = Field(alias="name")
    org_id: str = Field(alias="orgId")
    source_type: str = Field(alias="sourceType")
    status: str = Field(alias="status")
    updated_at: datetime = Field(alias="updatedAt")


class SetupSourceOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    source: SetupSource = Field(alias="source")


class SetupSourcesOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    sources: list[SetupSource] | None = Field(alias="sources")
    total: int = Field(alias="total")


class SetupSubmitSessionInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    events: list[PublicEvent] | None = Field(alias="events")


class SetupTestSession(ResponseModel):
    completed_at: datetime | None = Field(default=None, alias="completedAt", exclude=False)
    control_id: str = Field(alias="controlId")
    created_at: datetime = Field(alias="createdAt")
    diff: SetupSessionDiff | None = Field(default=None, alias="diff", exclude=False)
    expected_roles: list[str] | None = Field(alias="expectedRoles")
    expires_at: datetime = Field(alias="expiresAt")
    id: str = Field(alias="id")
    instructions: dict[str, Any] | None = Field(default=None, alias="instructions", exclude=False)
    observed_roles: list[str] | None = Field(alias="observedRoles")
    org_id: str = Field(alias="orgId")
    retry_count: int = Field(alias="retryCount")
    status: str = Field(alias="status")


class SignoffOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    signoff: PublicSignoff = Field(alias="signoff")


class SignoffRequestBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    approval_note: str | None = Field(default=None, alias="approvalNote", exclude=False)
    signed_with_exceptions: bool | None = Field(
        default=None, alias="signedWithExceptions", exclude=False
    )
    signer_name: str = Field(alias="signerName")
    signer_title: str | None = Field(default=None, alias="signerTitle", exclude=False)


class Source(ResponseModel):
    created_at: datetime = Field(alias="createdAt")
    id: str = Field(alias="id")
    name: str = Field(alias="name")
    org_id: str = Field(alias="orgId")
    schema_mapping: SchemaMap = Field(alias="schemaMapping")
    updated_at: datetime = Field(alias="updatedAt")


class SourceOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    source: Source = Field(alias="source")


class SourceRef(ResponseModel):
    display_name: str | None = Field(default=None, alias="display_name", exclude=False)
    role: SourceRefRole = Field(alias="role")
    source_id: str = Field(alias="source_id")


class StatusOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    status: str = Field(alias="status")


class Transaction(ResponseModel):
    amount_minor: int = Field(alias="amountMinor")
    currency: str = Field(alias="currency")
    date: str = Field(alias="date")
    direction: str = Field(alias="direction")
    id: str = Field(alias="id")
    idempotency_key: str = Field(alias="idempotencyKey")
    ingested_at: datetime = Field(alias="ingestedAt")
    metadata: Any | None = Field(default=None, alias="metadata", exclude=False)
    name: str | None = Field(default=None, alias="name", exclude=False)
    org_id: str = Field(alias="orgId")
    period_key: str = Field(alias="periodKey")
    raw: Any | None = Field(default=None, alias="raw", exclude=False)
    reference: str | None = Field(default=None, alias="reference", exclude=False)
    source_id: str = Field(alias="sourceId")
    status: str = Field(alias="status")
    transaction_type: str | None = Field(default=None, alias="transactionType", exclude=False)
    value_date: str | None = Field(default=None, alias="valueDate", exclude=False)


class TransactionDetailResource(ResponseModel):
    alerts: list[AlertLink] | None = Field(alias="alerts")
    amount_minor: int = Field(alias="amountMinor")
    correlation_namespace: str | None = Field(
        default=None, alias="correlationNamespace", exclude=False
    )
    currency: str = Field(alias="currency")
    direction: str = Field(alias="direction")
    entity_reference: str | None = Field(default=None, alias="entityReference", exclude=False)
    event_type: str = Field(alias="eventType")
    external_reference: str | None = Field(default=None, alias="externalReference", exclude=False)
    finding_id: str | None = Field(default=None, alias="findingId", exclude=False)
    findings: list[Issue] | None = Field(alias="findings")
    id: str = Field(alias="id")
    occurred_at: datetime = Field(alias="occurredAt")
    operation_id: str | None = Field(default=None, alias="operationId", exclude=False)
    provider_event_id: str | None = Field(default=None, alias="providerEventId", exclude=False)
    provider_reference: str | None = Field(default=None, alias="providerReference", exclude=False)
    received_at: datetime = Field(alias="receivedAt")
    reconciliation_links: list[ReconciliationLink] | None = Field(alias="reconciliationLinks")
    reconciliation_status: str | None = Field(
        default=None, alias="reconciliationStatus", exclude=False
    )
    related_events: list[RelatedEvent] | None = Field(alias="relatedEvents")
    signed_amount_minor: int = Field(alias="signedAmountMinor")
    source_event_id: str = Field(alias="sourceEventId")
    status: TransactionDetailResourceStatus = Field(alias="status")
    superseded: bool = Field(alias="superseded")
    supersedes_source_event_id: str | None = Field(
        default=None, alias="supersedesSourceEventId", exclude=False
    )
    wallet_id: str = Field(alias="walletId")


class TransactionOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    transaction: TransactionDetailResource = Field(alias="transaction")


class TransactionPage(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    next_cursor: str | None = Field(default=None, alias="nextCursor", exclude=False)
    transactions: list[WalletTransaction] | None = Field(alias="transactions")


class UpdateSourceInputBody(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    name: str | None = Field(default=None, alias="name", exclude=False)
    schema_mapping: SchemaMap | None = Field(default=None, alias="schemaMapping", exclude=False)


class UpdateSourceRequest(RequestModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    config: dict[str, Any] | None = Field(default=None, alias="config", exclude=False)
    name: str | None = Field(default=None, alias="name", exclude=False)
    status: str | None = Field(default=None, alias="status", exclude=False)


class Wallet(ResponseModel):
    balance_minor: int = Field(alias="balanceMinor")
    balance_updated_at: datetime | None = Field(
        default=None, alias="balanceUpdatedAt", exclude=False
    )
    created_at: datetime = Field(alias="createdAt")
    currency: str | None = Field(alias="currency")
    event_count: int = Field(alias="eventCount")
    has_additional_currencies: bool = Field(alias="hasAdditionalCurrencies")
    id: str = Field(alias="id")
    last_applied_at: datetime | None = Field(default=None, alias="lastAppliedAt", exclude=False)
    name: str = Field(alias="name")
    status: str = Field(alias="status")
    updated_at: datetime = Field(alias="updatedAt")


class WalletBalance(ResponseModel):
    balance_minor: int = Field(alias="balanceMinor")
    currency: str | None = Field(alias="currency")
    event_count: int = Field(alias="eventCount")
    has_additional_currencies: bool = Field(alias="hasAdditionalCurrencies")
    last_applied_at: datetime | None = Field(default=None, alias="lastAppliedAt", exclude=False)
    updated_at: datetime | None = Field(default=None, alias="updatedAt", exclude=False)
    wallet_id: str = Field(alias="walletId")


class WalletBalanceOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    balance: WalletBalance = Field(alias="balance")


class WalletOutputBody(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    wallet: Wallet = Field(alias="wallet")


class WalletPage(ResponseModel):
    schema_: str | None = Field(default=None, alias="$schema", exclude=True)
    limit: int = Field(alias="limit")
    offset: int = Field(alias="offset")
    total: int = Field(alias="total")
    wallets: list[Wallet] | None = Field(alias="wallets")


class WalletTransaction(ResponseModel):
    amount_minor: int = Field(alias="amountMinor")
    correlation_namespace: str | None = Field(
        default=None, alias="correlationNamespace", exclude=False
    )
    currency: str = Field(alias="currency")
    direction: str = Field(alias="direction")
    entity_reference: str | None = Field(default=None, alias="entityReference", exclude=False)
    event_type: str = Field(alias="eventType")
    external_reference: str | None = Field(default=None, alias="externalReference", exclude=False)
    finding_id: str | None = Field(default=None, alias="findingId", exclude=False)
    id: str = Field(alias="id")
    occurred_at: datetime = Field(alias="occurredAt")
    operation_id: str | None = Field(default=None, alias="operationId", exclude=False)
    provider_event_id: str | None = Field(default=None, alias="providerEventId", exclude=False)
    provider_reference: str | None = Field(default=None, alias="providerReference", exclude=False)
    received_at: datetime = Field(alias="receivedAt")
    reconciliation_status: str | None = Field(
        default=None, alias="reconciliationStatus", exclude=False
    )
    signed_amount_minor: int = Field(alias="signedAmountMinor")
    source_event_id: str = Field(alias="sourceEventId")
    status: WalletTransactionStatus = Field(alias="status")
    superseded: bool = Field(alias="superseded")
    supersedes_source_event_id: str | None = Field(
        default=None, alias="supersedesSourceEventId", exclude=False
    )
    wallet_id: str = Field(alias="walletId")


class AlertRuleRequest(RequestModel):
    breach_enabled: bool = Field(alias="breachEnabled")
    channels: list[str] | None = Field(default=None, alias="channels")
    control_id: str = Field(alias="controlId")
    dedup_window_seconds: int = Field(alias="dedupWindowSeconds")
    destinations: dict[str, Any] = Field(alias="destinations")
    resolution_enabled: bool = Field(alias="resolutionEnabled")
    severity_min: str = Field(alias="severityMin")
    suppressed_until: datetime | None = Field(default=None, alias="suppressedUntil")
    suppression_reason: str | None = Field(default=None, alias="suppressionReason")


def model_dump(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(by_alias=True, exclude_none=True, exclude_unset=True)


for _model in list(globals().values()):
    if isinstance(_model, type) and issubclass(_model, BaseModel) and _model is not BaseModel:
        _model.model_rebuild()
