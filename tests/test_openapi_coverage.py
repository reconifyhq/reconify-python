from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from reconify.resources import OPERATION_SPECS, SYNC_RESOURCE_CLASSES


def _openapi_path() -> Path | None:
    candidates = []
    if os.getenv("RECONIFY_OPENAPI_SPEC"):
        candidates.append(Path(os.environ["RECONIFY_OPENAPI_SPEC"]))
    candidates.append(Path(__file__).parents[1] / ".contract" / "reconify.openapi.json")
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def _operations() -> list[tuple[str, str, str]]:
    path = _openapi_path()
    if path is None:
        pytest.skip("OpenAPI source is not available; run scripts/fetch_contract.py")
    document = json.loads(path.read_text())
    return [
        (operation["operationId"], method.upper(), route.removeprefix("/v1") or "/")
        for route, methods in document["paths"].items()
        for method, operation in methods.items()
        if method.lower() in {"get", "post", "put", "patch", "delete"}
    ]


def test_openapi_contains_only_public_routes() -> None:
    path = _openapi_path()
    if path is None:
        pytest.skip("OpenAPI source is not available; run scripts/fetch_contract.py")
    document = json.loads(path.read_text())
    assert all(not route.startswith("/business/") for route in document["paths"])


def test_every_openapi_operation_has_a_public_method() -> None:
    operations = _operations()
    assert len(operations) == 13
    assert len({operation_id for operation_id, _, _ in operations}) == len(operations)
    assert len(OPERATION_SPECS) == len(operations)
    for operation_id, verb, route in operations:
        method_name = operation_id.replace("-", "_")
        assert method_name in OPERATION_SPECS, f"Missing SDK contract for {operation_id}"
        group, registered_verb, registered_route = OPERATION_SPECS[method_name]
        assert registered_route == route
        assert registered_verb == verb
        assert hasattr(SYNC_RESOURCE_CLASSES[group], method_name), (
            f"Missing SDK method for {operation_id}"
        )


def test_legacy_operations_are_not_public() -> None:
    legacy_names = {
        "list_ledger_sources",
        "list_wallets",
        "list_setup_sources",
        "search_integrity_resources",
        "list_alert_rules",
        "list_reconciliations",
    }
    assert not legacy_names.intersection(OPERATION_SPECS)
