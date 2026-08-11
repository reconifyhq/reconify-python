"""Organization resource client."""

from __future__ import annotations

from typing import Any

from ..models import ListMembersResponse
from ..models import Organization as OrganizationModel
from .base import AsyncResource, SyncResource


class Organization(SyncResource):
    def get_organization(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET", "/organization", params=query, response_model=OrganizationModel, raw=raw
        )

    def list_organization_members(self, raw: bool = False, **query: Any) -> Any:
        return self._request(
            "GET",
            "/organization/members",
            params=query,
            response_model=ListMembersResponse,
            raw=raw,
        )


class AsyncOrganization(AsyncResource):
    async def get_organization(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET", "/organization", params=query, response_model=OrganizationModel, raw=raw
        )

    async def list_organization_members(self, raw: bool = False, **query: Any) -> Any:
        return await self._request(
            "GET",
            "/organization/members",
            params=query,
            response_model=ListMembersResponse,
            raw=raw,
        )
