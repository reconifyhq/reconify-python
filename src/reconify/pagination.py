"""Synchronous and asynchronous helpers for Reconify page responses."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")


def iter_cursor_pages(
    fetch: Callable[..., Any],
    *,
    item_field: str,
    query: dict[str, Any] | None = None,
) -> Iterator[T]:
    """Yield items while passing the server's opaque ``nextCursor`` onward."""

    params = dict(query or {})
    params.pop("offset", None) if params.get("after") is not None else None
    while True:
        page = fetch(params)
        items = getattr(page, item_field, None) or []
        yield from items
        cursor = getattr(page, "next_cursor", None)
        if not cursor:
            return
        params["after"] = cursor
        if getattr(page, "limit", None) is not None and "limit" not in params:
            params["limit"] = page.limit


async def aiter_cursor_pages(
    fetch: Callable[..., Awaitable[Any]],
    *,
    item_field: str,
    query: dict[str, Any] | None = None,
) -> AsyncIterator[T]:
    """Async counterpart to :func:`iter_cursor_pages`."""

    params = dict(query or {})
    if params.get("after") is not None:
        params.pop("offset", None)
    while True:
        page = await fetch(params)
        items = getattr(page, item_field, None) or []
        for item in items:
            yield item
        cursor = getattr(page, "next_cursor", None)
        if not cursor:
            return
        params["after"] = cursor
        if getattr(page, "limit", None) is not None and "limit" not in params:
            params["limit"] = page.limit


def iter_offset_pages(
    fetch: Callable[..., Any],
    *,
    item_field: str,
    query: dict[str, Any] | None = None,
) -> Iterator[T]:
    """Yield items using the server-reported offset and total."""

    params = dict(query or {})
    params.pop("after", None)
    if params.get("offset") is None:
        params["offset"] = 0
    while True:
        page = fetch(params)
        items = list(getattr(page, item_field, None) or [])
        yield from items
        if not items:
            return
        offset = getattr(page, "offset", params["offset"])
        total = getattr(page, "total", None)
        next_offset = offset + len(items)
        if total is not None and next_offset >= total:
            return
        params["offset"] = next_offset
        if getattr(page, "limit", None) is not None and "limit" not in params:
            params["limit"] = page.limit


async def aiter_offset_pages(
    fetch: Callable[..., Awaitable[Any]],
    *,
    item_field: str,
    query: dict[str, Any] | None = None,
) -> AsyncIterator[T]:
    """Async counterpart to :func:`iter_offset_pages`."""

    params = dict(query or {})
    params.pop("after", None)
    if params.get("offset") is None:
        params["offset"] = 0
    while True:
        page = await fetch(params)
        items = list(getattr(page, item_field, None) or [])
        for item in items:
            yield item
        if not items:
            return
        offset = getattr(page, "offset", params["offset"])
        total = getattr(page, "total", None)
        next_offset = offset + len(items)
        if total is not None and next_offset >= total:
            return
        params["offset"] = next_offset
        if getattr(page, "limit", None) is not None and "limit" not in params:
            params["limit"] = page.limit
