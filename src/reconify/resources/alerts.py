"""Alerts API resource client."""

from __future__ import annotations

from typing import Any

from ..models import AlertRuleRequest, AlertRulesOutputBody, StatusOutputBody
from .base import AsyncResource, SyncResource


class Alerts(SyncResource):
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


class AsyncAlerts(AsyncResource):
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


OPERATION_SPECS = {
    "list_alert_rules": ("alerts", "GET", "/alerts/rules"),
    "put_alert_rule": ("alerts", "PUT", "/alerts/rules"),
}
