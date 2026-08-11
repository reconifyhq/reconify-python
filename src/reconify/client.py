"""Top-level synchronous and asynchronous Reconify clients."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from .errors import ReconifyValidationError
from .pagination import aiter_cursor_pages, iter_cursor_pages
from .resources import (
    ASYNC_RESOURCE_CLASSES,
    SYNC_RESOURCE_CLASSES,
    AsyncEvents,
    AsyncIngestion,
    AsyncIssues,
    AsyncMetadata,
    AsyncOrganization,
    Events,
    Ingestion,
    Issues,
    Metadata,
    Organization,
)
from .transport import AsyncTransport, RetryConfig, SyncTransport

DEFAULT_BASE_URL = "https://api.reconifyhq.com/v1"


def _normalize_base_url(base_url: str | None) -> str:
    value = (base_url or os.getenv("RECONIFY_API_URL") or DEFAULT_BASE_URL).rstrip("/")
    return value if value.endswith("/v1") else f"{value}/v1"


def _api_key(api_key: str | None) -> str:
    value = api_key or os.getenv("RECONIFY_API_KEY")
    if not value:
        raise ReconifyValidationError("An API key is required; set api_key or RECONIFY_API_KEY")
    if not value.startswith("rk_"):
        raise ReconifyValidationError("Reconify public API keys must start with rk_")
    return value


class Reconify:
    """Synchronous typed Reconify API client."""

    metadata: Metadata
    events: Events
    ingestion: Ingestion
    issues: Issues
    organization: Organization

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
        return iter_cursor_pages(
            lambda params: self.events.list_events(**params), item_field="events", query=query
        )

    def iter_issues(self, **query: Any) -> Iterator[Any]:
        return iter_cursor_pages(
            lambda params: self.issues.list_issues(**params), item_field="issues", query=query
        )

    def iter_issue_events(self, issue_id: str, **query: Any) -> Iterator[Any]:
        return iter_cursor_pages(
            lambda params: self.events.list_issue_events(issue_id, **params),
            item_field="events",
            query=query,
        )


class AsyncReconify:
    """Asynchronous typed Reconify API client."""

    metadata: AsyncMetadata
    events: AsyncEvents
    ingestion: AsyncIngestion
    issues: AsyncIssues
    organization: AsyncOrganization

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
        return aiter_cursor_pages(
            lambda params: self.events.list_events(**params), item_field="events", query=query
        )

    def iter_issues(self, **query: Any) -> AsyncIterator[Any]:
        return aiter_cursor_pages(
            lambda params: self.issues.list_issues(**params), item_field="issues", query=query
        )

    def iter_issue_events(self, issue_id: str, **query: Any) -> AsyncIterator[Any]:
        return aiter_cursor_pages(
            lambda params: self.events.list_issue_events(issue_id, **params),
            item_field="events",
            query=query,
        )
