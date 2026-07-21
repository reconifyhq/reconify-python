"""Shared implementation for resource clients."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote

from ..errors import ReconifyValidationError
from ..transport import AsyncTransport, SyncTransport

_PATH_PARAMETER_RE = re.compile(r"\{([^}]+)\}")


def _snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


class SyncResource:
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
        path_params = set(_PATH_PARAMETER_RE.findall(path))
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


class AsyncResource:
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
        path_params = set(_PATH_PARAMETER_RE.findall(path))
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
