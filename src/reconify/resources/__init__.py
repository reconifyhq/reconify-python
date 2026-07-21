"""Resource clients grouped by public API surface."""

from .alerts import Alerts, AsyncAlerts
from .events import AsyncEvents, Events
from .ingestion import AsyncIngestion, Ingestion
from .issues import AsyncIssues, Issues
from .ledger import AsyncLedger, Ledger
from .reconciliations import AsyncReconciliations, Reconciliations
from .search import AsyncSearch, Search
from .setup import AsyncSetup, Setup
from .transactions import AsyncTransactions, Transactions
from .wallets import AsyncWallets, Wallets

SYNC_RESOURCE_CLASSES = {
    "alerts": Alerts,
    "events": Events,
    "ingestion": Ingestion,
    "issues": Issues,
    "ledger": Ledger,
    "reconciliations": Reconciliations,
    "search": Search,
    "setup": Setup,
    "transactions": Transactions,
    "wallets": Wallets,
}
ASYNC_RESOURCE_CLASSES = {
    "alerts": AsyncAlerts,
    "events": AsyncEvents,
    "ingestion": AsyncIngestion,
    "issues": AsyncIssues,
    "ledger": AsyncLedger,
    "reconciliations": AsyncReconciliations,
    "search": AsyncSearch,
    "setup": AsyncSetup,
    "transactions": AsyncTransactions,
    "wallets": AsyncWallets,
}

OPERATION_SPECS = {
    "list_alert_rules": ("alerts", "GET", "/alerts/rules"),
    "put_alert_rule": ("alerts", "PUT", "/alerts/rules"),
    "list_events": ("events", "GET", "/events"),
    "get_event": ("events", "GET", "/events/{id}"),
    "reveal_event_field": ("events", "GET", "/events/{id}/reveal"),
    "ingest_integrity_events": ("ingestion", "POST", "/integrity/events"),
    "list_integrity_sources_for_reconciliation": ("reconciliations", "GET", "/integrity/sources"),
    "ingest_integrity_test_events": ("ingestion", "POST", "/integrity/test-events"),
    "list_issues": ("issues", "GET", "/issues"),
    "get_issue_summary": ("issues", "GET", "/issues/summary"),
    "get_issue": ("issues", "GET", "/issues/{id}"),
    "update_issue": ("issues", "PATCH", "/issues/{id}"),
    "list_issue_deliveries": ("issues", "GET", "/issues/{id}/deliveries"),
    "retry_issue_delivery": ("issues", "POST", "/issues/{id}/deliveries/{deliveryId}/retry"),
    "add_issue_note": ("issues", "POST", "/issues/{id}/notes"),
    "resolve_issue": ("issues", "POST", "/issues/{id}/resolve"),
    "list_ledger_sources": ("ledger", "GET", "/ledger/sources"),
    "create_ledger_source": ("ledger", "POST", "/ledger/sources"),
    "delete_ledger_source": ("ledger", "DELETE", "/ledger/sources/{id}"),
    "get_ledger_source": ("ledger", "GET", "/ledger/sources/{id}"),
    "update_ledger_source": ("ledger", "PATCH", "/ledger/sources/{id}"),
    "list_source_periods": ("ledger", "GET", "/ledger/sources/{id}/periods"),
    "list_transactions": ("ledger", "GET", "/ledger/sources/{id}/transactions"),
    "ingest_transactions": ("ledger", "POST", "/ledger/sources/{id}/transactions"),
    "list_reconciliation_schedules": ("reconciliations", "GET", "/reconciliation-schedules"),
    "create_reconciliation_schedule": ("reconciliations", "POST", "/reconciliation-schedules"),
    "delete_reconciliation_schedule": (
        "reconciliations",
        "DELETE",
        "/reconciliation-schedules/{id}",
    ),
    "get_reconciliation_schedule": ("reconciliations", "GET", "/reconciliation-schedules/{id}"),
    "update_reconciliation_schedule": (
        "reconciliations",
        "PATCH",
        "/reconciliation-schedules/{id}",
    ),
    "list_reconciliations": ("reconciliations", "GET", "/reconciliations"),
    "create_reconciliation": ("reconciliations", "POST", "/reconciliations"),
    "get_reconciliation": ("reconciliations", "GET", "/reconciliations/{id}"),
    "search_integrity_resources": ("search", "GET", "/search"),
    "list_setup_integrations": ("setup", "GET", "/setup/integrations"),
    "get_setup_integration": ("setup", "GET", "/setup/integrations/{id}"),
    "list_setup_sources": ("setup", "GET", "/setup/sources"),
    "create_setup_source": ("setup", "POST", "/setup/sources"),
    "get_setup_source": ("setup", "GET", "/setup/sources/{id}"),
    "update_setup_source": ("setup", "PATCH", "/setup/sources/{id}"),
    "disable_setup_source": ("setup", "DELETE", "/setup/sources/{id}"),
    "create_test_session": ("setup", "POST", "/setup/test-sessions"),
    "get_test_session": ("setup", "GET", "/setup/test-sessions/{id}"),
    "get_test_session_result": ("setup", "GET", "/setup/test-sessions/{id}/result"),
    "retry_test_session": ("setup", "POST", "/setup/test-sessions/{id}/retry"),
    "submit_test_session_events": ("setup", "POST", "/setup/test-sessions/{id}/submit"),
    "list_wallet_transactions": ("transactions", "GET", "/transactions"),
    "get_wallet_transaction": ("transactions", "GET", "/transactions/{id}"),
    "list_wallets": ("wallets", "GET", "/wallets"),
    "get_wallet": ("wallets", "GET", "/wallets/{id}"),
    "get_wallet_balance": ("wallets", "GET", "/wallets/{id}/balance"),
}

__all__ = [
    "Alerts",
    "AsyncAlerts",
    "AsyncEvents",
    "AsyncIngestion",
    "AsyncIssues",
    "AsyncLedger",
    "AsyncReconciliations",
    "AsyncSearch",
    "AsyncSetup",
    "AsyncTransactions",
    "AsyncWallets",
    "Events",
    "Ingestion",
    "Issues",
    "Ledger",
    "Reconciliations",
    "Search",
    "Setup",
    "Transactions",
    "Wallets",
    "ASYNC_RESOURCE_CLASSES",
    "OPERATION_SPECS",
    "SYNC_RESOURCE_CLASSES",
]
