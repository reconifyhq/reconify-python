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
    "api_info_get": ("metadata", "GET", "/"),
    "events_list": ("events", "GET", "/events"),
    "events_ingest": ("ingestion", "POST", "/events"),
    "events_get": ("events", "GET", "/events/{event_id}"),
    "health_get": ("metadata", "GET", "/health"),
    "issues_list": ("issues", "GET", "/issues"),
    "issues_get": ("issues", "GET", "/issues/{issue_id}"),
    "issues_assign": ("issues", "PATCH", "/issues/{issue_id}"),
    "issues_list_events": ("events", "GET", "/issues/{issue_id}/events"),
    "issues_list_notes": ("issues", "GET", "/issues/{issue_id}/notes"),
    "issues_add_note": ("issues", "POST", "/issues/{issue_id}/notes"),
    "organization_get": ("organization", "GET", "/organization"),
    "organization_list_members": ("organization", "GET", "/organization/members"),
}

OPERATION_METHODS = {
    "api_info_get": "get_api_info",
    "events_list": "list_events",
    "events_ingest": "ingest_monitoring_events",
    "events_get": "get_event",
    "health_get": "get_health",
    "issues_list": "list_issues",
    "issues_get": "get_issue",
    "issues_assign": "update_issue",
    "issues_list_events": "list_issue_events",
    "issues_list_notes": "list_issue_notes",
    "issues_add_note": "add_issue_note",
    "organization_get": "get_organization",
    "organization_list_members": "list_organization_members",
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
    "OPERATION_METHODS",
    "SYNC_RESOURCE_CLASSES",
]
