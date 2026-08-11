"""Resource clients grouped by the current public API surface."""

from .events import AsyncEvents, Events
from .ingestion import AsyncIngestion, Ingestion
from .issues import AsyncIssues, Issues
from .metadata import AsyncMetadata, Metadata
from .organization import AsyncOrganization, Organization

SYNC_RESOURCE_CLASSES = {
    "metadata": Metadata,
    "events": Events,
    "ingestion": Ingestion,
    "issues": Issues,
    "organization": Organization,
}
ASYNC_RESOURCE_CLASSES = {
    "metadata": AsyncMetadata,
    "events": AsyncEvents,
    "ingestion": AsyncIngestion,
    "issues": AsyncIssues,
    "organization": AsyncOrganization,
}

OPERATION_SPECS = {
    "get_api_info": ("metadata", "GET", "/"),
    "list_events": ("events", "GET", "/events"),
    "ingest_monitoring_events": ("ingestion", "POST", "/events"),
    "get_event": ("events", "GET", "/events/{event_id}"),
    "get_health": ("metadata", "GET", "/health"),
    "list_issues": ("issues", "GET", "/issues"),
    "get_issue": ("issues", "GET", "/issues/{issue_id}"),
    "update_issue": ("issues", "PATCH", "/issues/{issue_id}"),
    "list_issue_events": ("events", "GET", "/issues/{issue_id}/events"),
    "list_issue_notes": ("issues", "GET", "/issues/{issue_id}/notes"),
    "add_issue_note": ("issues", "POST", "/issues/{issue_id}/notes"),
    "get_organization": ("organization", "GET", "/organization"),
    "list_organization_members": ("organization", "GET", "/organization/members"),
}

__all__ = [
    "AsyncEvents",
    "AsyncIngestion",
    "AsyncIssues",
    "AsyncMetadata",
    "AsyncOrganization",
    "Events",
    "Ingestion",
    "Issues",
    "Metadata",
    "Organization",
    "ASYNC_RESOURCE_CLASSES",
    "OPERATION_SPECS",
    "SYNC_RESOURCE_CLASSES",
]
