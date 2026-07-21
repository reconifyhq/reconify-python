"""HTTP transport, retry policy, and raw response handling."""

from __future__ import annotations

import asyncio
import json
import random
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Generic, TypeVar, cast

import httpx
from pydantic import BaseModel, ValidationError

from .errors import ReconifyError, ReconifyValidationError, error_for_response
from .models import model_dump

T = TypeVar("T", bound=BaseModel)


@dataclass(frozen=True)
class RetryConfig:
    """Bounded retry settings. Retries apply to GET by default."""

    max_retries: int = 2
    base_delay: float = 0.25
    max_delay: float = 8.0
    jitter: float = 0.25
    retry_unsafe_methods: bool = False


@dataclass(frozen=True)
class RawResponse(Generic[T]):
    """Unparsed response data returned by an operation with ``raw=True``."""

    status_code: int
    headers: httpx.Headers
    body: bytes
    request_id: str | None

    def json(self) -> Any:
        return json.loads(self.body) if self.body else None


def _retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return max(0.0, (parsed - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return None


def _sleep_for(attempt: int, config: RetryConfig, retry_after: str | None) -> float:
    server_delay = _retry_after(retry_after)
    if server_delay is not None:
        return min(config.max_delay, server_delay)
    exponential = min(config.max_delay, config.base_delay * (2**attempt))
    return float(min(config.max_delay, exponential + random.uniform(0.0, config.jitter)))


def _can_retry_exception(method: str, attempts: int, config: RetryConfig) -> bool:
    if attempts >= config.max_retries:
        return False
    return method.upper() in {"GET", "HEAD", "OPTIONS"} or config.retry_unsafe_methods


def _payload(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except (ValueError, json.JSONDecodeError):
        return {"detail": response.text}


def _validate_request_body(body: Any) -> Any:
    if isinstance(body, BaseModel):
        try:
            return model_dump(body)
        except ValidationError as exc:
            raise ReconifyValidationError(str(exc)) from exc
    return body


def _validate_integrity_payload(path: str, body: Any) -> None:
    if path not in {"/integrity/events", "/integrity/test-events"} or body is None:
        return
    payload_size = len(json.dumps(body, separators=(",", ":"), default=str).encode("utf-8"))
    if payload_size > 5 * 1024 * 1024:
        raise ReconifyValidationError("Integrity event requests must not exceed 5 MiB")


class SyncTransport:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float | httpx.Timeout = 30.0,
        request_id: str | None = None,
        retry: RetryConfig | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.request_id = request_id
        self.retry = retry or RetryConfig()
        self._client = client or httpx.Client(timeout=timeout)
        self._owns_client = client is None

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: Any = None,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        raw: bool = False,
        timeout: float | httpx.Timeout | None = None,
    ) -> T | RawResponse[T] | None:
        request_headers = {"Authorization": f"Bearer {self.api_key}"}
        if body is not None:
            request_headers["Content-Type"] = "application/json"
        if self.request_id:
            request_headers["X-Request-ID"] = self.request_id
        request_headers.update(headers or {})
        data = _validate_request_body(body)
        _validate_integrity_payload(path, data)
        params = {key: value for key, value in (query or {}).items() if value is not None}
        attempts = 0
        while True:
            try:
                response = self._client.request(
                    method,
                    f"{self.base_url}{path}",
                    params=params,
                    json=data if data is not None else None,
                    headers=request_headers,
                    timeout=timeout,
                )
            except httpx.TransportError:
                if not _can_retry_exception(method, attempts, self.retry):
                    raise
                time.sleep(_sleep_for(attempts, self.retry, None))
                attempts += 1
                continue
            if response.status_code not in {429, 503} or not self._can_retry(method, attempts):
                return self._finish(response, model=model, raw=raw)
            delay = _sleep_for(attempts, self.retry, response.headers.get("Retry-After"))
            time.sleep(delay)
            attempts += 1

    def _can_retry(self, method: str, attempts: int) -> bool:
        if attempts >= self.retry.max_retries:
            return False
        return method.upper() in {"GET", "HEAD", "OPTIONS"} or self.retry.retry_unsafe_methods

    def _finish(
        self, response: httpx.Response, *, model: type[T] | None, raw: bool
    ) -> T | RawResponse[T] | None:
        request_id = response.headers.get("X-Request-ID")
        if response.is_error:
            raise error_for_response(
                response.status_code,
                dict(response.headers),
                _payload(response),
                request_id=request_id,
            )
        if response.status_code == 204:
            return None
        if raw:
            return RawResponse(response.status_code, response.headers, response.content, request_id)
        payload = _payload(response)
        if model is None or payload is None:
            return cast(T | RawResponse[T] | None, payload)
        try:
            return model.model_validate(payload)
        except ValidationError as exc:
            raise ReconifyError(
                "The Reconify response did not match the expected schema",
                status_code=response.status_code,
                request_id=request_id,
                response_headers=dict(response.headers),
            ) from exc

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


class AsyncTransport:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float | httpx.Timeout = 30.0,
        request_id: str | None = None,
        retry: RetryConfig | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.request_id = request_id
        self.retry = retry or RetryConfig()
        self._client = client or httpx.AsyncClient(timeout=timeout)
        self._owns_client = client is None

    async def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: Any = None,
        headers: dict[str, str] | None = None,
        model: type[T] | None = None,
        raw: bool = False,
        timeout: float | httpx.Timeout | None = None,
    ) -> T | RawResponse[T] | None:
        request_headers = {"Authorization": f"Bearer {self.api_key}"}
        if body is not None:
            request_headers["Content-Type"] = "application/json"
        if self.request_id:
            request_headers["X-Request-ID"] = self.request_id
        request_headers.update(headers or {})
        data = _validate_request_body(body)
        _validate_integrity_payload(path, data)
        params = {key: value for key, value in (query or {}).items() if value is not None}
        attempts = 0
        while True:
            try:
                response = await self._client.request(
                    method,
                    f"{self.base_url}{path}",
                    params=params,
                    json=data if data is not None else None,
                    headers=request_headers,
                    timeout=timeout,
                )
            except httpx.TransportError:
                if not _can_retry_exception(method, attempts, self.retry):
                    raise
                await asyncio.sleep(_sleep_for(attempts, self.retry, None))
                attempts += 1
                continue
            if response.status_code not in {429, 503} or not self._can_retry(method, attempts):
                return self._finish(response, model=model, raw=raw)
            delay = _sleep_for(attempts, self.retry, response.headers.get("Retry-After"))
            await asyncio.sleep(delay)
            attempts += 1

    def _can_retry(self, method: str, attempts: int) -> bool:
        if attempts >= self.retry.max_retries:
            return False
        return method.upper() in {"GET", "HEAD", "OPTIONS"} or self.retry.retry_unsafe_methods

    def _finish(
        self, response: httpx.Response, *, model: type[T] | None, raw: bool
    ) -> T | RawResponse[T] | None:
        request_id = response.headers.get("X-Request-ID")
        if response.is_error:
            raise error_for_response(
                response.status_code,
                dict(response.headers),
                _payload(response),
                request_id=request_id,
            )
        if response.status_code == 204:
            return None
        if raw:
            return RawResponse(response.status_code, response.headers, response.content, request_id)
        payload = _payload(response)
        if model is None or payload is None:
            return cast(T | RawResponse[T] | None, payload)
        try:
            return model.model_validate(payload)
        except ValidationError as exc:
            raise ReconifyError(
                "The Reconify response did not match the expected schema",
                status_code=response.status_code,
                request_id=request_id,
                response_headers=dict(response.headers),
            ) from exc

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
