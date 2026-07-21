"""Issues API resource client."""

from __future__ import annotations

from typing import Any

from ..models import (
    DeliveriesOutputBody,
    IssueCounts,
    IssueDetail,
    IssuePage,
    IssueUpdateInputBody,
    NoteInputBody,
    ResolveInputBody,
    StatusOutputBody,
)
from .base import AsyncResource, SyncResource


class Issues(SyncResource):
    def list_issues(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues",
            params=query,
            body=None,
            response_model=IssuePage,
            raw=raw,
        )

    def get_issue_summary(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues/summary",
            params=query,
            body=None,
            response_model=IssueCounts,
            raw=raw,
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


class AsyncIssues(AsyncResource):
    async def list_issues(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues",
            params=query,
            body=None,
            response_model=IssuePage,
            raw=raw,
        )

    async def get_issue_summary(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues/summary",
            params=query,
            body=None,
            response_model=IssueCounts,
            raw=raw,
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
            params={**query, "id": id, "delivery_id": delivery_id},
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


OPERATION_SPECS = {
    "list_issues": ("issues", "GET", "/issues"),
    "get_issue_summary": ("issues", "GET", "/issues/summary"),
    "get_issue": ("issues", "GET", "/issues/{id}"),
    "update_issue": ("issues", "PATCH", "/issues/{id}"),
    "list_issue_deliveries": ("issues", "GET", "/issues/{id}/deliveries"),
    "retry_issue_delivery": ("issues", "POST", "/issues/{id}/deliveries/{deliveryId}/retry"),
    "add_issue_note": ("issues", "POST", "/issues/{id}/notes"),
    "resolve_issue": ("issues", "POST", "/issues/{id}/resolve"),
}
