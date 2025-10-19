"""
LangSmith Monitoring and Observability Module
Provides functions to interact with LangSmith for monitoring and analysis
"""

from typing import Dict, List, Optional

from langsmith import Client

from src.infrastructure.config.settings import settings
from src.infrastructure.logging.logger import get_logger

# Module logger
logger = get_logger(__name__)


def get_langsmith_client() -> Client:
    """
    Creates and returns a LangSmith client instance.
    Uses Pydantic Settings for API key validation.

    Returns:
        Client: Configured LangSmith client
    """
    # Settings already validated API key exists
    return Client()


def get_project_info() -> Dict[str, str]:
    """
    Returns information about the current LangSmith project.

    Returns:
        Dictionary with project configuration
    """
    return {
        "project_name": settings.langsmith_project,
        "tracing_enabled": str(settings.langsmith_tracing).lower(),
        "endpoint": settings.langsmith_endpoint,
    }


def list_recent_runs(limit: int = 10) -> List:
    """
    Lists recent runs from the current project.

    Args:
        limit: Maximum number of runs to return

    Returns:
        List of recent run objects
    """
    try:
        client = get_langsmith_client()
        project_name = settings.langsmith_project

        runs = list(client.list_runs(project_name=project_name, limit=limit))

        return runs
    except Exception as e:
        logger.error(
            "error_listing_runs",
            project_name=settings.langsmith_project,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        return []


def get_run_stats(run_id: str) -> Optional[Dict]:
    """
    Gets detailed statistics for a specific run.

    Args:
        run_id: The ID of the run to analyze

    Returns:
        Dictionary with run statistics or None if not found
    """
    try:
        client = get_langsmith_client()
        run = client.read_run(run_id)

        return {
            "id": run.id,
            "name": run.name,
            "run_type": run.run_type,
            "start_time": run.start_time,
            "end_time": run.end_time,
            "latency_ms": run.latency_ms if hasattr(run, "latency_ms") else None,
            "total_tokens": run.total_tokens if hasattr(run, "total_tokens") else None,
            "status": run.status if hasattr(run, "status") else None,
        }
    except Exception as e:
        logger.error(
            "error_getting_run_stats",
            run_id=run_id,
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        return None


def print_monitoring_summary() -> None:
    """
    Prints a summary of LangSmith monitoring configuration and recent activity.
    """
    print("\n" + "=" * 80)
    print("LANGSMITH MONITORING SUMMARY")
    print("=" * 80)

    # Project info
    info = get_project_info()
    print("\nProject Configuration:")
    print(f"  - Project Name: {info['project_name']}")
    print(f"  - Tracing Enabled: {info['tracing_enabled']}")
    print(f"  - Endpoint: {info['endpoint']}")

    # Recent runs
    print("\nRecent Runs:")
    try:
        runs = list_recent_runs(limit=5)
        if runs:
            for i, run in enumerate(runs, 1):
                print(f"  {i}. {run.name} ({run.run_type}) - {run.id}")
        else:
            print("  No runs found or tracing not enabled")
    except Exception as e:
        print(f"  Error retrieving runs: {e}")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    # Test monitoring functions
    print_monitoring_summary()
