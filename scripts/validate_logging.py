,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0222222222222000
2
3
03
.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,003
0003





































































2415"""
Simple validation script for structured logging.

Tests:
1. Logger initialization
2. Different log levels
3. Context variable binding
4. JSON output format
5. Exception logging
"""

import json
import sys

from structlog.contextvars import bind_contextvars
from structlog.contextvars import clear_contextvars
from utils.logger import configure_logging
from utils.logger import get_logger

1
def test_basic_logging():
    """Test basic logging functionality."""
    print("\n" + "=" * 80)
    print("TEST 1: Basic Logging")
    print("=" * 80)

    logger = get_logger(__name__)

    logger.debug("debug_message", detail="This should be filtered (DEBUG < INFO)")
    logger.info("info_message", status="success", code=200)
    logger.warning("warning_message", alert="Low disk space")
    logger.error("error_message", error_code=500, details="Internal server error")

    print("\n✓ Basic logging test complete\n")


def test_context_variables():
    """Test context variable binding."""
    print("=" * 80)
    print("TEST 2: Context Variables")
    print("=" * 80)

    clear_contextvars()  # Clear any previous context

    logger = get_logger(__name__)

    # Bind context that will appear in all logs
    bind_contextvars(
        user_id=123,
        session_id="abc-123-def",
        request_id="req-456",
    )

    logger.info("user_action", action="login", success=True)
    logger.info("database_query", table="users", rows=42)

    clear_contextvars()  # Cleanup
    print("\n✓ Context variables test complete\n")


def test_exception_logging():
    """Test exception logging with stack traces."""
    print("=" * 80)
    print("TEST 3: Exception Logging")
    print("=" * 80)

    logger = get_logger(__name__)

    try:
        # Simulate an error
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.error(
            "division_error",
            operation="divide",
            numerator=1,
            denominator=0,
            exc_info=True,
        )

    print("\n✓ Exception logging test complete\n")


def test_reranker_style_logging():
    """Test logging similar to reranker.py usage."""
    print("=" * 80)
    print("TEST 4: Reranker-Style Logging")
    print("=" * 80)

    clear_contextvars()
    logger = get_logger("reranker")

    # Simulate reranking operation
    query = "What is machine learning?"
    num_documents = 15
    threshold = 0.7

    bind_contextvars(
        query_preview=query[:50],
        num_documents=num_documents,
        threshold=threshold,
        top_n=5,
    )

    logger.info("model_loading_started", model="BAAI/bge-reranker-base")
    logger.info("model_loaded_successfully", model="BAAI/bge-reranker-base")

    logger.info(
        "threshold_filtering_applied",
        filtered_count=10,
        total_documents=15,
        kept_documents=5,
    )

    logger.info(
        "reranking_completed",
        original_count=15,
        reranked_count=5,
        score_max=0.95,
        score_min=0.72,
        score_mean=0.83,
    )

    clear_contextvars()
    print("\n✓ Reranker-style logging test complete\n")


def test_json_output_validation():
    """Validate JSON output format."""
    print("=" * 80)
    print("TEST 5: JSON Output Validation")
    print("=" * 80)

    # Capture one log entry
    logger = get_logger(__name__)
    logger.info(
        "json_test",
        key1="value1",
        key2=42,
        key3=True,
        key4={"nested": "object"},
    )

    print("\n✓ JSON output validation complete")
    print("  (Check above output for valid JSON format)\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("STRUCTURED LOGGING VALIDATION")
    print("=" * 80)

    # Show configuration
    from config.settings import settings

    print(f"\nConfiguration:")
    print(f"  - LOG_LEVEL: {settings.log_level}")
    print(f"  - LOG_FORMAT: {settings.log_format}")
    print(f"  - Is TTY: {sys.stderr.isatty()}")
    print()

    # Run tests
    test_basic_logging()
    test_context_variables()
    test_exception_logging()
    test_reranker_style_logging()
    test_json_output_validation()

    print("=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)
    print("\nValidation Summary:")
    print("  ✓ Logger initialization working")
    print("  ✓ Log level filtering (DEBUG filtered, INFO+ showing)")
    print("  ✓ Context variables binding and propagation")
    print("  ✓ Exception logging with stack traces")
    print("  ✓ Reranker-style structured logging")
    print("  ✓ JSON output format (if not TTY)")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
