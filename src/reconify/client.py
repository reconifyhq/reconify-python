"""Top-level synchronous and asynchronous Reconify clients."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from .errors import ReconifyValidationError
from .pagination import (
    aiter_cursor_pages,
    aiter_offset_pages,
    iter_cursor_pages,
    iter_offset_pages,
)
from .resources import (
    ASYNC_RESOURCE_CLASSES,
    SYNC_RESOURCE_CLASSES,
    Alerts,
    AsyncAlerts,
    AsyncEvents,
    AsyncIngestion,
    AsyncIssues,
    AsyncLedger,
    AsyncReconciliations,
    AsyncSearch,
    AsyncSetup,
    AsyncTransactions,
    AsyncWallets,
    Events,
    Ingestion,
    Issues,
    Ledger,
    Reconciliations,
    Search,
    Setup,
    Transactions,
    Wallets,
)
from .transport import AsyncTransport, RetryConfig, SyncTransport

DEFAULT_BASE_URL = "https://api.reconifyhq.com/v1"


def _normalize_base_url(base_url: str | None) -> str:
    value = (base_url or os.getenv("RECONIFY_API_URL") or DEFAULT_BASE_URL).rstrip("/")
    return value if value.endswith("/v1") else f"{value}/v1"


def _api_key(api_key: str | None) -> str:
    value = api_key or os.getenv("RECONIFY_API_KEY")
    if not value:
        raise ReconifyValidationError("An API key is required")
    if value.startswith("sk_live_"):
        raise ReconifyValidationError("Legacy sk_live_ keys are not supported; use an rk_ key")
    if not value.startswith("rk_"):
        raise ReconifyValidationError("Reconify public API keys must start with rk_")
    return value


class Reconify:
    """Synchronous typed Reconify API client."""

    alerts: Alerts
    events: Events
    ingestion: Ingestion
    issues: Issues
    ledger: Ledger
    reconciliations: Reconciliations
    search: Search
    setup: Setup
    transactions: Transactions
    wallets: Wallets

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout = 30.0,
        request_id: str | None = None,
        retry: RetryConfig | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._transport = SyncTransport(
            base_url=_normalize_base_url(base_url),
            api_key=_api_key(api_key),
            timeout=timeout,
            request_id=request_id,
            retry=retry,
            client=http_client,
        )
        for name, resource_class in SYNC_RESOURCE_CLASSES.items():
            setattr(self, name, resource_class(self._transport))

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> Reconify:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def iter_events(self, **query: Any) -> Iterator[Any]:
        return iter_cursor_pages(self.events.list_events, item_field="events", query=query)

    def iter_issues(self, **query: Any) -> Iterator[Any]:
        return iter_cursor_pages(self.issues.list_issues, item_field="issues", query=query)

    def iter_ledger_sources(self, **query: Any) -> Iterator[Any]:
        return iter_offset_pages(self.ledger.list_ledger_sources, item_field="sources", query=query)

    def iter_ledger_transactions(self, source_id: str, **query: Any) -> Iterator[Any]:
        return iter_offset_pages(
            lambda params: self.ledger.list_transactions(source_id, **params),
            item_field="transactions",
            query=query,
        )

    def iter_reconciliation_schedules(self, **query: Any) -> Iterator[Any]:
        return iter_offset_pages(
            self.reconciliations.list_reconciliation_schedules,
            item_field="schedules",
            query=query,
        )

    def iter_reconciliations(self, **query: Any) -> Iterator[Any]:
        return iter_offset_pages(
            self.reconciliations.list_reconciliations,
            item_field="reconciliations",
            query=query,
        )

    def iter_setup_sources(self, **query: Any) -> Iterator[Any]:
        return iter_offset_pages(self.setup.list_setup_sources, item_field="sources", query=query)

    def iter_wallet_transactions(self, **query: Any) -> Iterator[Any]:
        return iter_cursor_pages(
            self.transactions.list_wallet_transactions,
            item_field="transactions",
            query=query,
        )

    def iter_wallets(self, **query: Any) -> Iterator[Any]:
        return iter_offset_pages(self.wallets.list_wallets, item_field="wallets", query=query)


class AsyncReconify:
    """Asynchronous typed Reconify API client."""

    alerts: AsyncAlerts
    events: AsyncEvents
    ingestion: AsyncIngestion
    issues: AsyncIssues
    ledger: AsyncLedger
    reconciliations: AsyncReconciliations
    search: AsyncSearch
    setup: AsyncSetup
    transactions: AsyncTransactions
    wallets: AsyncWallets

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout = 30.0,
        request_id: str | None = None,
        retry: RetryConfig | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._transport = AsyncTransport(
            base_url=_normalize_base_url(base_url),
            api_key=_api_key(api_key),
            timeout=timeout,
            request_id=request_id,
            retry=retry,
            client=http_client,
        )
        for name, resource_class in ASYNC_RESOURCE_CLASSES.items():
            setattr(self, name, resource_class(self._transport))

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncReconify:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    def iter_events(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_cursor_pages(self.events.list_events, item_field="events", query=query)

    def iter_issues(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_cursor_pages(self.issues.list_issues, item_field="issues", query=query)

    def iter_ledger_sources(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_offset_pages(
            self.ledger.list_ledger_sources, item_field="sources", query=query
        )

    def iter_ledger_transactions(self, source_id: str, **query: Any) -> AsyncIterator[Any]:
        return aiter_offset_pages(
            lambda params: self.ledger.list_transactions(source_id, **params),
            item_field="transactions",
            query=query,
        )

    def iter_reconciliation_schedules(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_offset_pages(
            self.reconciliations.list_reconciliation_schedules,
            item_field="schedules",
            query=query,
        )

    def iter_reconciliations(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_offset_pages(
            self.reconciliations.list_reconciliations,
            item_field="reconciliations",
            query=query,
        )

    def iter_setup_sources(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_offset_pages(self.setup.list_setup_sources, item_field="sources", query=query)

    def iter_wallet_transactions(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_cursor_pages(
            self.transactions.list_wallet_transactions,
            item_field="transactions",
            query=query,
        )

    def iter_wallets(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_offset_pages(self.wallets.list_wallets, item_field="wallets", query=query)
