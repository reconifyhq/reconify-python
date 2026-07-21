"""Exception types and safe error parsing for Reconify responses."""

from __future__ import annotations

from typing import Any, cast


class ReconifyError(Exception):
    """Base class for client, validation, transport, and API errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        title: str | None = None,
        detail: str | None = None,
        code: str | None = None,
        validation_errors: list[dict[str, Any]] | None = None,
        request_id: str | None = None,
        response_headers: dict[str, str] | None = None,
        response_metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.code = code
        self.validation_errors = validation_errors or []
        self.request_id = request_id
        self.response_headers = response_headers or {}
        self.response_metadata = response_metadata or {}


class ReconifyValidationError(ReconifyError):
    """The client rejected invalid arguments before making a request."""


class ReconifyAuthenticationError(ReconifyError):
    """The API key is missing or not accepted (HTTP 401)."""


class ReconifyPermissionError(ReconifyError):
    """The API key cannot access the requested resource (HTTP 403)."""


class ReconifyNotFoundError(ReconifyError):
    """The requested resource does not exist (HTTP 404)."""


class ReconifyConflictError(ReconifyError):
    """The request conflicts with current server state (HTTP 409)."""


class ReconifyRequestError(ReconifyError):
    """The request is malformed or fails validation (HTTP 400/422)."""


class ReconifyRateLimitError(ReconifyError):
    """The API rate limit was exceeded (HTTP 429)."""


class ReconifyServiceUnavailableError(ReconifyError):
    """The API is temporarily unavailable (HTTP 503)."""


class ReconifyServerError(ReconifyError):
    """The API returned an unexpected 5xx response."""


_STATUS_ERRORS: dict[int, type[ReconifyError]] = {
    400: ReconifyRequestError,
    401: ReconifyAuthenticationError,
    403: ReconifyPermissionError,
    404: ReconifyNotFoundError,
    409: ReconifyConflictError,
    422: ReconifyRequestError,
    429: ReconifyRateLimitError,
    500: ReconifyServerError,
    503: ReconifyServiceUnavailableError,
}


def error_for_response(
    status_code: int,
    headers: dict[str, str],
    payload: Any,
    *,
    request_id: str | None,
) -> ReconifyError:
    """Build a typed exception without including credentials or request bodies."""

    data = payload if isinstance(payload, dict) else {}
    title = data.get("title") if isinstance(data.get("title"), str) else None
    detail = data.get("detail") if isinstance(data.get("detail"), str) else None
    if detail is None and isinstance(data.get("error"), str):
        detail = data["error"]
    if detail is None and isinstance(data.get("message"), str):
        detail = data["message"]

    validation = data.get("errors") if isinstance(data.get("errors"), list) else []
    validation = cast(list[Any], validation)
    safe_validation = [item for item in validation if isinstance(item, dict)]
    code = None
    for item in safe_validation:
        if item.get("location") == "$code" and isinstance(item.get("message"), str):
            code = item["message"]
            break
    if code is None and isinstance(data.get("code"), str):
        code = data["code"]

    message = detail or title or f"Reconify API request failed with status {status_code}"
    exception_type = _STATUS_ERRORS.get(
        status_code,
        ReconifyServerError if status_code >= 500 else ReconifyError,
    )
    metadata = {
        key: value
        for key, value in data.items()
        if key not in {"detail", "message", "error", "errors"}
    }
    return exception_type(
        message,
        status_code=status_code,
        title=title,
        detail=detail,
        code=code,
        validation_errors=safe_validation,
        request_id=request_id,
        response_headers=headers,
        response_metadata=metadata,
    )
