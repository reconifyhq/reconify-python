"""Resource clients for the retained Reconify Public API operations."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote

from .errors import ReconifyValidationError
from .models import (
    AlertRuleRequest,
    AlertRulesOutputBody,
    BatchResponse,
    CreateReconciliationInputBody,
    CreateSessionRequest,
    CreateSourceInputBody,
    CreateSourceRequest,
    DeliveriesOutputBody,
    EventDetail,
    EventPage,
    EventRevealOutputBody,
    IngestEventsInputBody,
    IngestTransactionsInputBody,
    IngestTransactionsOutputBody,
    IssueCounts,
    IssueDetail,
    IssuePage,
    IssueUpdateInputBody,
    ListIntegritySourcesOutputBody,
    ListPeriodsOutputBody,
    ListReconciliationsOutputBody,
    ListSchedulesOutputBody,
    ListSourcesOutputBody,
    ListTransactionsOutputBody,
    NoteInputBody,
    ReconciliationOutputBody,
    ResolveInputBody,
    ScheduleOutputBody,
    ScheduleRequestBody,
    ScheduleUpdateRequestBody,
    SearchPage,
    SetupIntegrationOutputBody,
    SetupIntegrationsOutputBody,
    SetupSessionOutputBody,
    SetupSourceOutputBody,
    SetupSourcesOutputBody,
    SetupSubmitSessionInputBody,
    SourceOutputBody,
    StatusOutputBody,
    TransactionOutputBody,
    TransactionPage,
    UpdateSourceInputBody,
    UpdateSourceRequest,
    WalletBalanceOutputBody,
    WalletOutputBody,
    WalletPage,
)
from .transport import AsyncTransport, SyncTransport

_PATH_PARAMETER_RE = re.compile(r"\{([^}]+)\}")


class _SyncResource:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any],
        body: Any = None,
        response_model: Any = None,
        raw: bool = False,
        headers: dict[str, str] | None = None,
    ) -> Any:
        path_params = {name for name in _PATH_PARAMETER_RE.findall(path)}
        wire_params = dict(params)
        for name in path_params:
            python_name = _snake(name)
            if python_name not in wire_params or wire_params[python_name] is None:
                raise ReconifyValidationError(f"Missing required path parameter: {python_name}")
            path = path.replace("{" + name + "}", quote(str(wire_params.pop(python_name)), safe=""))
        request_headers = dict(headers or {})
        if wire_params.get("integrity_test_session"):
            request_headers["X-Integrity-Test-Session"] = wire_params.pop("integrity_test_session")
        if wire_params.get("after") is not None:
            wire_params.pop("offset", None)
        return self._transport.request(
            method,
            path,
            query=wire_params,
            body=body,
            headers=request_headers,
            model=response_model,
            raw=raw,
        )


class _AsyncResource:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any],
        body: Any = None,
        response_model: Any = None,
        raw: bool = False,
        headers: dict[str, str] | None = None,
    ) -> Any:
        path_params = {name for name in _PATH_PARAMETER_RE.findall(path)}
        wire_params = dict(params)
        for name in path_params:
            python_name = _snake(name)
            if python_name not in wire_params or wire_params[python_name] is None:
                raise ReconifyValidationError(f"Missing required path parameter: {python_name}")
            path = path.replace("{" + name + "}", quote(str(wire_params.pop(python_name)), safe=""))
        request_headers = dict(headers or {})
        if wire_params.get("integrity_test_session"):
            request_headers["X-Integrity-Test-Session"] = wire_params.pop("integrity_test_session")
        if wire_params.get("after") is not None:
            wire_params.pop("offset", None)
        return await self._transport.request(
            method,
            path,
            query=wire_params,
            body=body,
            headers=request_headers,
            model=response_model,
            raw=raw,
        )


def _snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


class Alerts(_SyncResource):
    def list_alert_rules(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/alerts/rules",
            params=query,
            body=None,
            response_model=AlertRulesOutputBody,
            raw=raw,
        )

    def put_alert_rule(self, body: AlertRuleRequest, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "PUT",
            "/alerts/rules",
            params=query,
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )


class Events(_SyncResource):
    def list_events(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/events", params=query, body=None, response_model=EventPage, raw=raw
        )

    def get_event(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/events/{id}",
            params={**query, "id": id},
            body=None,
            response_model=EventDetail,
            raw=raw,
        )

    def reveal_event_field(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/events/{id}/reveal",
            params={**query, "id": id},
            body=None,
            response_model=EventRevealOutputBody,
            raw=raw,
        )


class Ingestion(_SyncResource):
    def ingest_integrity_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return self._request(
            "POST",
            "/integrity/events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )

    def ingest_integrity_test_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return self._request(
            "POST",
            "/integrity/test-events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


class Issues(_SyncResource):
    def list_issues(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/issues", params=query, body=None, response_model=IssuePage, raw=raw
        )

    def get_issue_summary(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/issues/summary", params=query, body=None, response_model=IssueCounts, raw=raw
        )

    def get_issue(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues/{id}",
            params={**query, "id": id},
            body=None,
            response_model=IssueDetail,
            raw=raw,
        )

    def update_issue(
        self, id: str, body: IssueUpdateInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/issues/{id}",
            params={**query, "id": id},
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )

    def list_issue_deliveries(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues/{id}/deliveries",
            params={**query, "id": id},
            body=None,
            response_model=DeliveriesOutputBody,
            raw=raw,
        )

    def retry_issue_delivery(
        self, id: str, delivery_id: str, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/issues/{id}/deliveries/{deliveryId}/retry",
            params={**query, "id": id, "delivery_id": delivery_id},
            body=None,
            response_model=StatusOutputBody,
            raw=raw,
        )

    def add_issue_note(self, id: str, body: NoteInputBody, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "POST",
            "/issues/{id}/notes",
            params={**query, "id": id},
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )

    def resolve_issue(
        self, id: str, body: ResolveInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/issues/{id}/resolve",
            params={**query, "id": id},
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )


class Ledger(_SyncResource):
    def list_ledger_sources(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources",
            params=query,
            body=None,
            response_model=ListSourcesOutputBody,
            raw=raw,
        )

    def create_ledger_source(
        self, body: CreateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/ledger/sources",
            params=query,
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    def delete_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "DELETE",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    def get_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SourceOutputBody,
            raw=raw,
        )

    def update_ledger_source(
        self, id: str, body: UpdateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    def list_source_periods(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources/{id}/periods",
            params={**query, "id": id},
            body=None,
            response_model=ListPeriodsOutputBody,
            raw=raw,
        )

    def list_transactions(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=None,
            response_model=ListTransactionsOutputBody,
            raw=raw,
        )

    def ingest_transactions(
        self, id: str, body: IngestTransactionsInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=body,
            response_model=IngestTransactionsOutputBody,
            raw=raw,
        )


class Reconciliations(_SyncResource):
    def list_integrity_sources_for_reconciliation(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/integrity/sources",
            params=query,
            body=None,
            response_model=ListIntegritySourcesOutputBody,
            raw=raw,
        )

    def list_reconciliation_schedules(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliation-schedules",
            params=query,
            body=None,
            response_model=ListSchedulesOutputBody,
            raw=raw,
        )

    def create_reconciliation_schedule(
        self, body: ScheduleRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/reconciliation-schedules",
            params=query,
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    def delete_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "DELETE",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    def get_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    def update_reconciliation_schedule(
        self, id: str, body: ScheduleUpdateRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    def list_reconciliations(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliations",
            params=query,
            body=None,
            response_model=ListReconciliationsOutputBody,
            raw=raw,
        )

    def create_reconciliation(
        self, body: CreateReconciliationInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/reconciliations",
            params=query,
            body=body,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )

    def get_reconciliation(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/reconciliations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )


class Search(_SyncResource):
    def search_integrity_resources(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/search", params=query, body=None, response_model=SearchPage, raw=raw
        )


class Setup(_SyncResource):
    def list_setup_integrations(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/integrations",
            params=query,
            body=None,
            response_model=SetupIntegrationsOutputBody,
            raw=raw,
        )

    def get_setup_integration(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/integrations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupIntegrationOutputBody,
            raw=raw,
        )

    def list_setup_sources(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/sources",
            params=query,
            body=None,
            response_model=SetupSourcesOutputBody,
            raw=raw,
        )

    def create_setup_source(
        self, body: CreateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/setup/sources",
            params=query,
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    def get_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    def update_setup_source(
        self, id: str, body: UpdateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    def disable_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "DELETE",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    def create_test_session(
        self, body: CreateSessionRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "POST",
            "/setup/test-sessions",
            params=query,
            body=body,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def get_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/test-sessions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def get_test_session_result(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/setup/test-sessions/{id}/result",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def retry_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "POST",
            "/setup/test-sessions/{id}/retry",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    def submit_test_session_events(
        self,
        id: str,
        body: SetupSubmitSessionInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return self._request(
            "POST",
            "/setup/test-sessions/{id}/submit",
            params={**query, "id": id},
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


class Transactions(_SyncResource):
    def list_wallet_transactions(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/transactions", params=query, body=None, response_model=TransactionPage, raw=raw
        )

    def get_wallet_transaction(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/transactions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=TransactionOutputBody,
            raw=raw,
        )


class Wallets(_SyncResource):
    def list_wallets(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/wallets", params=query, body=None, response_model=WalletPage, raw=raw
        )

    def get_wallet(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/wallets/{id}",
            params={**query, "id": id},
            body=None,
            response_model=WalletOutputBody,
            raw=raw,
        )

    def get_wallet_balance(self, id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/wallets/{id}/balance",
            params={**query, "id": id},
            body=None,
            response_model=WalletBalanceOutputBody,
            raw=raw,
        )


class AsyncAlerts(_AsyncResource):
    async def list_alert_rules(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/alerts/rules",
            params=query,
            body=None,
            response_model=AlertRulesOutputBody,
            raw=raw,
        )

    async def put_alert_rule(self, body: AlertRuleRequest, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "PUT",
            "/alerts/rules",
            params=query,
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )


class AsyncEvents(_AsyncResource):
    async def list_events(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/events", params=query, body=None, response_model=EventPage, raw=raw
        )

    async def get_event(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/events/{id}",
            params={**query, "id": id},
            body=None,
            response_model=EventDetail,
            raw=raw,
        )

    async def reveal_event_field(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/events/{id}/reveal",
            params={**query, "id": id},
            body=None,
            response_model=EventRevealOutputBody,
            raw=raw,
        )


class AsyncIngestion(_AsyncResource):
    async def ingest_integrity_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return await self._request(
            "POST",
            "/integrity/events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )

    async def ingest_integrity_test_events(
        self,
        body: IngestEventsInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return await self._request(
            "POST",
            "/integrity/test-events",
            params=query,
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


class AsyncIssues(_AsyncResource):
    async def list_issues(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/issues", params=query, body=None, response_model=IssuePage, raw=raw
        )

    async def get_issue_summary(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/issues/summary", params=query, body=None, response_model=IssueCounts, raw=raw
        )

    async def get_issue(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues/{id}",
            params={**query, "id": id},
            body=None,
            response_model=IssueDetail,
            raw=raw,
        )

    async def update_issue(
        self, id: str, body: IssueUpdateInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/issues/{id}",
            params={**query, "id": id},
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )

    async def list_issue_deliveries(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues/{id}/deliveries",
            params={**query, "id": id},
            body=None,
            response_model=DeliveriesOutputBody,
            raw=raw,
        )

    async def retry_issue_delivery(
        self, id: str, delivery_id: str, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/issues/{id}/deliveries/{deliveryId}/retry",
            params={**query, id: id, delivery_id: delivery_id},
            body=None,
            response_model=StatusOutputBody,
            raw=raw,
        )

    async def add_issue_note(
        self, id: str, body: NoteInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/issues/{id}/notes",
            params={**query, "id": id},
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )

    async def resolve_issue(
        self, id: str, body: ResolveInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/issues/{id}/resolve",
            params={**query, "id": id},
            body=body,
            response_model=StatusOutputBody,
            raw=raw,
        )


class AsyncLedger(_AsyncResource):
    async def list_ledger_sources(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources",
            params=query,
            body=None,
            response_model=ListSourcesOutputBody,
            raw=raw,
        )

    async def create_ledger_source(
        self, body: CreateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/ledger/sources",
            params=query,
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    async def delete_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "DELETE",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    async def get_ledger_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SourceOutputBody,
            raw=raw,
        )

    async def update_ledger_source(
        self, id: str, body: UpdateSourceInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/ledger/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SourceOutputBody,
            raw=raw,
        )

    async def list_source_periods(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources/{id}/periods",
            params={**query, "id": id},
            body=None,
            response_model=ListPeriodsOutputBody,
            raw=raw,
        )

    async def list_transactions(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=None,
            response_model=ListTransactionsOutputBody,
            raw=raw,
        )

    async def ingest_transactions(
        self, id: str, body: IngestTransactionsInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/ledger/sources/{id}/transactions",
            params={**query, "id": id},
            body=body,
            response_model=IngestTransactionsOutputBody,
            raw=raw,
        )


class AsyncReconciliations(_AsyncResource):
    async def list_integrity_sources_for_reconciliation(
        self, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "GET",
            "/integrity/sources",
            params=query,
            body=None,
            response_model=ListIntegritySourcesOutputBody,
            raw=raw,
        )

    async def list_reconciliation_schedules(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliation-schedules",
            params=query,
            body=None,
            response_model=ListSchedulesOutputBody,
            raw=raw,
        )

    async def create_reconciliation_schedule(
        self, body: ScheduleRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/reconciliation-schedules",
            params=query,
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    async def delete_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "DELETE",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    async def get_reconciliation_schedule(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    async def update_reconciliation_schedule(
        self, id: str, body: ScheduleUpdateRequestBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/reconciliation-schedules/{id}",
            params={**query, "id": id},
            body=body,
            response_model=ScheduleOutputBody,
            raw=raw,
        )

    async def list_reconciliations(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliations",
            params=query,
            body=None,
            response_model=ListReconciliationsOutputBody,
            raw=raw,
        )

    async def create_reconciliation(
        self, body: CreateReconciliationInputBody, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/reconciliations",
            params=query,
            body=body,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )

    async def get_reconciliation(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/reconciliations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=ReconciliationOutputBody,
            raw=raw,
        )


class AsyncSearch(_AsyncResource):
    async def search_integrity_resources(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/search", params=query, body=None, response_model=SearchPage, raw=raw
        )


class AsyncSetup(_AsyncResource):
    async def list_setup_integrations(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/integrations",
            params=query,
            body=None,
            response_model=SetupIntegrationsOutputBody,
            raw=raw,
        )

    async def get_setup_integration(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/integrations/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupIntegrationOutputBody,
            raw=raw,
        )

    async def list_setup_sources(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/sources",
            params=query,
            body=None,
            response_model=SetupSourcesOutputBody,
            raw=raw,
        )

    async def create_setup_source(
        self, body: CreateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/setup/sources",
            params=query,
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    async def get_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    async def update_setup_source(
        self, id: str, body: UpdateSourceRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=body,
            response_model=SetupSourceOutputBody,
            raw=raw,
        )

    async def disable_setup_source(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "DELETE",
            "/setup/sources/{id}",
            params={**query, "id": id},
            body=None,
            response_model=None,
            raw=raw,
        )

    async def create_test_session(
        self, body: CreateSessionRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "POST",
            "/setup/test-sessions",
            params=query,
            body=body,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def get_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/test-sessions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def get_test_session_result(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/setup/test-sessions/{id}/result",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def retry_test_session(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "POST",
            "/setup/test-sessions/{id}/retry",
            params={**query, "id": id},
            body=None,
            response_model=SetupSessionOutputBody,
            raw=raw,
        )

    async def submit_test_session_events(
        self,
        id: str,
        body: SetupSubmitSessionInputBody,
        integrity_test_session: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        return await self._request(
            "POST",
            "/setup/test-sessions/{id}/submit",
            params={**query, "id": id},
            body=body,
            response_model=BatchResponse,
            raw=raw,
            headers={"X-Integrity-Test-Session": integrity_test_session}
            if integrity_test_session
            else None,
        )


class AsyncTransactions(_AsyncResource):
    async def list_wallet_transactions(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/transactions", params=query, body=None, response_model=TransactionPage, raw=raw
        )

    async def get_wallet_transaction(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/transactions/{id}",
            params={**query, "id": id},
            body=None,
            response_model=TransactionOutputBody,
            raw=raw,
        )


class AsyncWallets(_AsyncResource):
    async def list_wallets(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/wallets", params=query, body=None, response_model=WalletPage, raw=raw
        )

    async def get_wallet(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/wallets/{id}",
            params={**query, "id": id},
            body=None,
            response_model=WalletOutputBody,
            raw=raw,
        )

    async def get_wallet_balance(self, id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/wallets/{id}/balance",
            params={**query, "id": id},
            body=None,
            response_model=WalletBalanceOutputBody,
            raw=raw,
        )


SYNC_RESOURCE_CLASSES = {
    "alerts": Alerts,
    "events": Events,
    "ingestion": Ingestion,
    "issues": Issues,
    "ledger": Ledger,
    "reconciliations": Reconciliations,
    "search": Search,
    "setup": Setup,
    "transactions": Transactions,
    "wallets": Wallets,
}
ASYNC_RESOURCE_CLASSES = {
    "alerts": AsyncAlerts,
    "events": AsyncEvents,
    "ingestion": AsyncIngestion,
    "issues": AsyncIssues,
    "ledger": AsyncLedger,
    "reconciliations": AsyncReconciliations,
    "search": AsyncSearch,
    "setup": AsyncSetup,
    "transactions": AsyncTransactions,
    "wallets": AsyncWallets,
}


# Stable operation registry used by the OpenAPI coverage test and tooling.
OPERATION_SPECS = {
    "list_alert_rules": ("alerts", "GET", "/alerts/rules"),
    "put_alert_rule": ("alerts", "PUT", "/alerts/rules"),
    "list_events": ("events", "GET", "/events"),
    "get_event": ("events", "GET", "/events/{id}"),
    "reveal_event_field": ("events", "GET", "/events/{id}/reveal"),
    "ingest_integrity_events": ("ingestion", "POST", "/integrity/events"),
    "list_integrity_sources_for_reconciliation": ("reconciliations", "GET", "/integrity/sources"),
    "ingest_integrity_test_events": ("ingestion", "POST", "/integrity/test-events"),
    "list_issues": ("issues", "GET", "/issues"),
    "get_issue_summary": ("issues", "GET", "/issues/summary"),
    "get_issue": ("issues", "GET", "/issues/{id}"),
    "update_issue": ("issues", "PATCH", "/issues/{id}"),
    "list_issue_deliveries": ("issues", "GET", "/issues/{id}/deliveries"),
    "retry_issue_delivery": ("issues", "POST", "/issues/{id}/deliveries/{deliveryId}/retry"),
    "add_issue_note": ("issues", "POST", "/issues/{id}/notes"),
    "resolve_issue": ("issues", "POST", "/issues/{id}/resolve"),
    "list_ledger_sources": ("ledger", "GET", "/ledger/sources"),
    "create_ledger_source": ("ledger", "POST", "/ledger/sources"),
    "delete_ledger_source": ("ledger", "DELETE", "/ledger/sources/{id}"),
    "get_ledger_source": ("ledger", "GET", "/ledger/sources/{id}"),
    "update_ledger_source": ("ledger", "PATCH", "/ledger/sources/{id}"),
    "list_source_periods": ("ledger", "GET", "/ledger/sources/{id}/periods"),
    "list_transactions": ("ledger", "GET", "/ledger/sources/{id}/transactions"),
    "ingest_transactions": ("ledger", "POST", "/ledger/sources/{id}/transactions"),
    "list_reconciliation_schedules": ("reconciliations", "GET", "/reconciliation-schedules"),
    "create_reconciliation_schedule": ("reconciliations", "POST", "/reconciliation-schedules"),
    "delete_reconciliation_schedule": (
        "reconciliations",
        "DELETE",
        "/reconciliation-schedules/{id}",
    ),
    "get_reconciliation_schedule": ("reconciliations", "GET", "/reconciliation-schedules/{id}"),
    "update_reconciliation_schedule": (
        "reconciliations",
        "PATCH",
        "/reconciliation-schedules/{id}",
    ),
    "list_reconciliations": ("reconciliations", "GET", "/reconciliations"),
    "create_reconciliation": ("reconciliations", "POST", "/reconciliations"),
    "get_reconciliation": ("reconciliations", "GET", "/reconciliations/{id}"),
    "search_integrity_resources": ("search", "GET", "/search"),
    "list_setup_integrations": ("setup", "GET", "/setup/integrations"),
    "get_setup_integration": ("setup", "GET", "/setup/integrations/{id}"),
    "list_setup_sources": ("setup", "GET", "/setup/sources"),
    "create_setup_source": ("setup", "POST", "/setup/sources"),
    "get_setup_source": ("setup", "GET", "/setup/sources/{id}"),
    "update_setup_source": ("setup", "PATCH", "/setup/sources/{id}"),
    "disable_setup_source": ("setup", "DELETE", "/setup/sources/{id}"),
    "create_test_session": ("setup", "POST", "/setup/test-sessions"),
    "get_test_session": ("setup", "GET", "/setup/test-sessions/{id}"),
    "get_test_session_result": ("setup", "GET", "/setup/test-sessions/{id}/result"),
    "retry_test_session": ("setup", "POST", "/setup/test-sessions/{id}/retry"),
    "submit_test_session_events": ("setup", "POST", "/setup/test-sessions/{id}/submit"),
    "list_wallet_transactions": ("transactions", "GET", "/transactions"),
    "get_wallet_transaction": ("transactions", "GET", "/transactions/{id}"),
    "list_wallets": ("wallets", "GET", "/wallets"),
    "get_wallet": ("wallets", "GET", "/wallets/{id}"),
    "get_wallet_balance": ("wallets", "GET", "/wallets/{id}/balance"),
}
