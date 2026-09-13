"""Pydantic models for the current Reconify public OpenAPI contract."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TolerantStrEnum(str, Enum):
    """String enum that preserves values added by a compatible API release."""

    @classmethod
    def _missing_(cls, value: object) -> TolerantStrEnum | None:
        if isinstance(value, str):
            member = str.__new__(cls, value)
            member._name_ = "UNKNOWN_" + value.upper().replace("-", "_").replace(".", "_")
            member._value_ = value
            cls._value2member_map_[value] = member
            return member
        return None


class ResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True, validate_assignment=True)


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)


class Flow(TolerantStrEnum):
    PAYMENT_TO_WALLET = "payment_to_wallet"
    PAYMENT_TO_ORDER = "payment_to_order"
    WALLET_TO_WALLET = "wallet_to_wallet"
    WALLET_TO_PAYOUT = "wallet_to_payout"
    PROVIDER_TO_SETTLEMENT_ACCOUNT = "provider_to_settlement_account"


class EventType(TolerantStrEnum):
    ORDER_FULFILLED = "order.fulfilled"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_INITIATED = "payment.initiated"
    PAYMENT_SUCCEEDED = "payment.succeeded"
    PAYOUT_FAILED = "payout.failed"
    PAYOUT_INITIATED = "payout.initiated"
    PAYOUT_SUCCEEDED = "payout.succeeded"
    WALLET_CREDITED = "wallet.credited"
    WALLET_DEBITED = "wallet.debited"
    WALLET_REFUNDED = "wallet.refunded"
    SETTLEMENT_ALLOCATIONS_RECORDED = "settlement.allocations_recorded"
    SETTLEMENT_CREATED = "settlement.created"
    SETTLEMENT_DISBURSED = "settlement.disbursed"
    SETTLEMENT_FAILED = "settlement.failed"
    SETTLEMENT_FINALIZED = "settlement.finalized"
    SETTLEMENT_RECEIVED = "settlement.received"
    SETTLEMENT_REVISED = "settlement.revised"


class EntityType(TolerantStrEnum):
    WALLET = "wallet"
    ORDER = "order"


class ReceiptStatus(TolerantStrEnum):
    RECEIVED = "received"
    PUBLISHED = "published"
    PROCESSED = "processed"
    FAILED = "failed"


class IssueStatus(TolerantStrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    RESOLVED_LATE = "resolved_late"


class IssueCategory(TolerantStrEnum):
    BUSINESS_FAILURE = "business_failure"
    MISSING_EVENT = "missing_event"
    MISMATCH = "mismatch"
    DUPLICATE_OR_CONFLICT = "duplicate_or_conflict"


class Severity(TolerantStrEnum):
    HIGH = "high"
    MEDIUM = "medium"


class MemberRole(TolerantStrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class MonitoringResultStatus(TolerantStrEnum):
    ACCEPTED = "accepted"
    DUPLICATE = "duplicate"
    REJECTED = "rejected"


class MonitoringErrorCode(TolerantStrEnum):
    INVALID_EVENT = "invalid_event"
    UNKNOWN_FIELD = "unknown_field"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    DUPLICATE = "duplicate"
    MALFORMED_REQUEST = "malformed_request"


class OnchainSourceKind(TolerantStrEnum):
    PROVIDER_PAYMENT = "provider_payment"
    TRANSACTION = "transaction"
    ADDRESS_REFERENCE = "address_reference"


class OnchainNetwork(TolerantStrEnum):
    ETHEREUM_MAINNET = "ethereum-mainnet"
    ETHEREUM_SEPOLIA = "ethereum-sepolia"
    SOLANA_MAINNET = "solana-mainnet"
    SOLANA_DEVNET = "solana-devnet"


class OnchainSourceStatus(TolerantStrEnum):
    QUEUED = "queued"


class FinancialComponentKind(TolerantStrEnum):
    FEE = "fee"
    COMMISSION = "commission"
    TAX = "tax"
    RESERVE = "reserve"
    ADJUSTMENT = "adjustment"
    OTHER = "other"


class FinancialComponentEffect(TolerantStrEnum):
    ADD = "add"
    DEDUCT = "deduct"
    INCLUDED = "included"


class SettlementAllocationType(TolerantStrEnum):
    PAYMENT = "payment"
    REFUND = "refund"
    CHARGEBACK = "chargeback"


class APIInfo(ResponseModel):
    name: str
    version: str
    documentation_url: str
    status_url: str


class Health(ResponseModel):
    status: str


class FinancialComponent(RequestModel):
    amount: str
    kind: FinancialComponentKind
    effect: FinancialComponentEffect
    description: str | None = None
    provider_type: str | None = None
    reference: str | None = None
    metadata: dict[str, str | int | float | bool] | None = None


class FinancialBreakdown(RequestModel):
    gross: str
    net: str
    components: list[FinancialComponent] = Field(max_length=100)


class SettlementAllocation(RequestModel):
    allocation_id: str
    allocation_type: SettlementAllocationType
    flow: str
    reference: str
    amount: str
    event_id: str | None = None


class MonitoringEventData(RequestModel):
    provider: str | None = None
    integration_ref: str | None = None
    provider_transaction_id: str | None = None
    provider_reference: str | None = None
    failure_code: str | None = None
    failure_message: str | None = None
    retryable: bool | None = None
    revises_event_id: str | None = None
    allocations: list[SettlementAllocation] | None = Field(default=None, max_length=500)


class MonitoringEvent(RequestModel):
    id: str | None = None
    flow: Flow
    type: EventType
    reference: str
    entity_id: str
    occurred_at: datetime | None = None
    amount: str | None = None
    correlation_id: str | None = None
    causation_id: str | None = None
    currency: str | None = None
    data: MonitoringEventData | None = None
    financial_breakdown: FinancialBreakdown | None = None
    metadata: dict[str, str | int | float | bool] | None = None


class MonitoringBatchRequest(RequestModel):
    events: list[MonitoringEvent] = Field(min_length=1, max_length=500)


class MonitoringResult(ResponseModel):
    index: int
    status: MonitoringResultStatus
    event_id: str | None = None
    code: MonitoringErrorCode | None = None
    field: str | None = None
    message: str | None = None
    warnings: list[str] | None = None


class MonitoringBatchResponse(ResponseModel):
    results: list[MonitoringResult]


class MonitoringSchema(ResponseModel):
    limits: dict[str, int] | None = None
    warnings: list[str] | None = None
    error_codes: list[str] | None = None


class Event(ResponseModel):
    id: str
    flow: Flow
    event_type: EventType
    reference: str
    entity_type: EntityType
    entity_id: str
    occurred_at: datetime
    received_at: datetime
    amount: str | None = None
    currency: str | None = None
    causation_id: str | None = None
    correlation_id: str | None = None
    revises_event_id: str | None = None
    provider: str | None = None
    status: ReceiptStatus
    gross: str | None = None
    net: str | None = None
    component_count: int | None = None
    allocation_count: int | None = None
    financial_breakdown: FinancialBreakdown | None = None
    allocations: list[SettlementAllocation] | None = None


class ListEventsResponse(ResponseModel):
    events: list[Event]
    limit: int
    next_cursor: str | None = None


class Issue(ResponseModel):
    id: str
    status: IssueStatus
    category: IssueCategory
    severity: Severity
    message: str
    assigned_to: str | None = None
    operation_id: str | None = None
    opened_at: datetime
    resolved_at: datetime | None = None


class ListIssuesResponse(ResponseModel):
    issues: list[Issue]
    limit: int
    next_cursor: str | None = None


class PatchIssueRequest(RequestModel):
    assigned_to: str | None


class Note(ResponseModel):
    id: str | None = None
    author_user_id: str | None = None
    body: str
    created_at: datetime | None = None


class AddNoteRequest(RequestModel):
    body: str = Field(min_length=1, max_length=10_000)


class ListNotesResponse(ResponseModel):
    notes: list[Note]


class Organization(ResponseModel):
    id: str
    name: str
    slug: str
    created_at: datetime


class Member(ResponseModel):
    id: str
    role: MemberRole
    joined_at: datetime


class ListMembersResponse(ResponseModel):
    members: list[Member]


class Error(ResponseModel):
    code: str | None = None
    message: str | None = None
    title: str | None = None
    status: int | None = None
    detail: str | None = None


class OnchainSourceLocator(RequestModel):
    integration_ref: str | None = None
    network: OnchainNetwork | None = None
    protocol_reference: str | None = None
    provider_reference: str | None = None
    provider_transaction_id: str | None = None
    receiving_address: str | None = None
    transaction_reference: str | None = None
    window_end: datetime | None = None
    window_start: datetime | None = None


class OnchainSourceRequest(RequestModel):
    flow: str
    operation_reference: str = Field(min_length=1, max_length=256)
    source_event_id: str = Field(min_length=1, max_length=256)
    kind: OnchainSourceKind
    locator: OnchainSourceLocator


class OnchainSourceResponse(ResponseModel):
    id: str
    status: OnchainSourceStatus
    duplicate: bool


def model_dump(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(mode="json", by_alias=True, exclude_none=True, exclude_unset=True)
