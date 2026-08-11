"""Issue investigation resource client."""

from __future__ import annotations

from typing import Any

from ..models import (
    AddNoteRequest,
    Issue,
    ListIssuesResponse,
    ListNotesResponse,
    Note,
    PatchIssueRequest,
)
from .base import AsyncResource, SyncResource


class Issues(SyncResource):
    def list_issues(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/issues", params=query, response_model=ListIssuesResponse, raw=raw
        )

    def get_issue(self, issue_id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues/{issue_id}",
            params={**query, "issue_id": issue_id},
            response_model=Issue,
            raw=raw,
        )

    def update_issue(
        self, issue_id: str, body: PatchIssueRequest, raw: bool = False, **query: Any
    ) -> Any:
        return self._request(
            "PATCH",
            "/issues/{issue_id}",
            params={**query, "issue_id": issue_id},
            body=body,
            response_model=Issue,
            raw=raw,
        )

    def list_issue_notes(self, issue_id: str, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/issues/{issue_id}/notes",
            params={**query, "issue_id": issue_id},
            response_model=ListNotesResponse,
            raw=raw,
        )

    def add_issue_note(
        self,
        issue_id: str,
        body: AddNoteRequest,
        *,
        idempotency_key: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._request(
            "POST",
            "/issues/{issue_id}/notes",
            params={**query, "issue_id": issue_id},
            body=body,
            response_model=Note,
            raw=raw,
            headers=headers,
        )


class AsyncIssues(AsyncResource):
    async def list_issues(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/issues", params=query, response_model=ListIssuesResponse, raw=raw
        )

    async def get_issue(self, issue_id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues/{issue_id}",
            params={**query, "issue_id": issue_id},
            response_model=Issue,
            raw=raw,
        )

    async def update_issue(
        self, issue_id: str, body: PatchIssueRequest, raw: bool = False, **query: Any
    ) -> Any:
        return await self._request(
            "PATCH",
            "/issues/{issue_id}",
            params={**query, "issue_id": issue_id},
            body=body,
            response_model=Issue,
            raw=raw,
        )

    async def list_issue_notes(self, issue_id: str, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/issues/{issue_id}/notes",
            params={**query, "issue_id": issue_id},
            response_model=ListNotesResponse,
            raw=raw,
        )

    async def add_issue_note(
        self,
        issue_id: str,
        body: AddNoteRequest,
        *,
        idempotency_key: str | None = None,
        raw: bool = False,
        **query: Any,
    ) -> Any:
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return await self._request(
            "POST",
            "/issues/{issue_id}/notes",
            params={**query, "issue_id": issue_id},
            body=body,
            response_model=Note,
            raw=raw,
            headers=headers,
        )
