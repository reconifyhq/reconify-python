from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from reconify.resources import OPERATION_SPECS, SYNC_RESOURCE_CLASSES

EXCLUDED_PATHS = {
    "/reconciliations/{id}/adjustments",
    "/reconciliations/{id}/adjustments/{adjustment_id}",
    "/reconciliations/{id}/close",
    "/reconciliations/{id}/reopen",
    "/reconciliations/{id}/evidence",
    "/reconciliations/{id}/evidence/{evidence_id}",
    "/reconciliations/{id}/reports/reconciliation/items",
    "/reconciliations/{id}/signoffs",
    "/reconciliations/{id}/signoffs/{role}",
}


def _openapi_path() -> Path | None:
    candidates = []
    if os.getenv("RECONIFY_OPENAPI_PATH"):
        candidates.append(Path(os.environ["RECONIFY_OPENAPI_PATH"]))
    candidates.append(
        Path(
            "/Users/koladev/conductor/workspaces/reconify-saas/pattaya/openapi/reconify.openapi.json"
        )
    )
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def _operations() -> list[tuple[str, str]]:
    path = _openapi_path()
    if path is None:
        pytest.skip("OpenAPI source is not available; set RECONIFY_OPENAPI_PATH")
    document = json.loads(path.read_text())
    return [
        (operation["operationId"], route)
        for route, methods in document["paths"].items()
        for method, operation in methods.items()
        if method.lower() in {"get", "post", "put", "patch", "delete"}
        and route not in EXCLUDED_PATHS
    ]


def test_openapi_requires_exactly_fifty_retained_operations() -> None:
    operations = _operations()
    assert len(operations) == 50
    assert len(OPERATION_SPECS) == 50


def test_every_retained_openapi_operation_has_a_public_method() -> None:
    operations = _operations()
    for operation_id, route in operations:
        method_name = operation_id.replace("-", "_")
        assert method_name in OPERATION_SPECS, f"Missing SDK contract for {operation_id}"
        group, verb, registered_route = OPERATION_SPECS[method_name]
        assert registered_route == route
        assert verb in {"GET", "POST", "PUT", "PATCH", "DELETE"}
        assert hasattr(SYNC_RESOURCE_CLASSES[group], method_name), (
            f"Missing SDK method for {operation_id}"
        )


def test_excluded_reconciliation_operations_are_not_public() -> None:
    excluded_ids = {
        "list_reconciliation_adjustments",
        "create_reconciliation_adjustment",
        "get_reconciliation_adjustment",
        "close_reconciliation",
        "reopen_reconciliation",
        "list_reconciliation_evidence",
        "create_reconciliation_evidence",
        "get_reconciliation_evidence",
        "list_reconciliation_items",
        "list_reconciliation_signoffs",
        "upsert_reconciliation_signoff",
        "delete_reconciliation_signoff",
    }
    assert not any(
        hasattr(SYNC_RESOURCE_CLASSES["reconciliations"], method_name)
        for method_name in excluded_ids
    )
    assert not excluded_ids.intersection(OPERATION_SPECS)
