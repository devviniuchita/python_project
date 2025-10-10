"""
Tests for structured logging with structlog.

Validates:
1. Logger configuration (JSON vs console based on environment)
2. Context variable binding and propagation
3. Log level filtering
4. Exception formatting
5. Performance overhead (<5ms target)
"""

import json
import logging
import sys

from io import StringIO
from unittest.mock import patch

import pytest
import structlog

from utils.logger import configure_logging
from utils.logger import get_logger


class TestLoggingConfiguration:
    """Test logger configuration and initialization."""

    def test_logger_returns_bound_logger(self):
        """Verify get_logger returns a BoundLogger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, structlog.stdlib.BoundLogger)

    def test_logger_with_name(self):
        """Verify logger accepts custom names."""
        logger = get_logger("test.module")
        assert logger is not None

    def test_logger_without_name(self):
        """Verify logger works without name (root logger)."""
        logger = get_logger()
        assert logger is not None


class TestContextVariables:
    """Test context variable binding and propagation."""

    def test_context_binding(self, capfd):
        """Verify context variables are included in logs."""
        from structlog.contextvars import bind_contextvars
        from structlog.contextvars import clear_contextvars

        # Clear any previous context
        clear_contextvars()

        # Bind context variables
        bind_contextvars(user_id=123, request_id="abc-123")

        logger = get_logger(__name__)
        logger.info("test_event", action="testing")

        # Capture output
        out, err = capfd.readouterr()
        output = out + err

        # Parse JSON if in JSON mode, otherwise check string contains
        if "{" in output:
            # JSON mode
            log_entry = json.loads(output.strip().split("\n")[0])
            assert log_entry.get("user_id") == 123
            assert log_entry.get("request_id") == "abc-123"
            assert log_entry.get("event") == "test_event"
            assert log_entry.get("action") == "testing"
        else:
            # Console mode - check string contains values
            assert "user_id" in output or "123" in output
            assert "request_id" in output or "abc-123" in output

        # Cleanup
        clear_contextvars()


class TestLogLevelFiltering:
    """Test log level filtering."""

    def test_debug_filtered_when_info_level(self, capfd):
        """Verify DEBUG logs are filtered when level is INFO."""
        logger = get_logger(__name__)

        # Try to log DEBUG (should be filtered)
        logger.debug("debug_message", detail="should_not_appear")

        # Log INFO (should appear)
        logger.info("info_message", detail="should_appear")

        out, err = capfd.readouterr()
        output = out + err

        # DEBUG should not appear
        assert "debug_message" not in output
        assert "should_not_appear" not in output

        # INFO should appear
        assert "info_message" in output or "should_appear" in output

    def test_error_logged_when_info_level(self, capfd):
        """Verify ERROR logs appear when level is INFO."""
        logger = get_logger(__name__)

        logger.error("error_message", code=500)

        out, err = capfd.readouterr()
        output = out + err

        assert "error_message" in output or "500" in output


class TestExceptionFormatting:
    """Test exception logging and formatting."""

    def test_exception_logging(self, capfd):
        """Verify exceptions are properly formatted in logs."""
        logger = get_logger(__name__)

        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.error("exception_occurred", exc_info=True)

        out, err = capfd.readouterr()
        output = out + err

        # Should contain exception info
        assert "ValueError" in output or "Test exception" in output
        assert "exception_occurred" in output


class TestJSONOutput:
    """Test JSON output format (production mode)."""

    def test_json_output_format(self, capfd):
        """Verify JSON output contains required fields."""
        logger = get_logger(__name__)
        logger.info("test_json", key="value", number=42)

        out, err = capfd.readouterr()
        output = (out + err).strip()

        # If JSON mode, verify structure
        if output.startswith("{"):
            log_entry = json.loads(output.split("\n")[0])

            # Check standard fields
            assert "event" in log_entry
            assert "timestamp" in log_entry
            assert "level" in log_entry

            # Check custom fields
            assert log_entry.get("event") == "test_json"
            assert log_entry.get("key") == "value"
            assert log_entry.get("number") == 42


class TestPerformance:
    """Test logging performance overhead."""

    def test_logging_performance(self, benchmark):
        """Verify logging overhead is <5ms per entry."""
        logger = get_logger(__name__)

        def log_operation():
            logger.info(
                "performance_test",
                query="test query",
                num_docs=10,
                score=0.95,
            )

        # Benchmark should complete in <5ms
        result = benchmark(log_operation)
        assert result.stats.mean < 0.005  # 5ms in seconds


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    # Reconfigure on each test to ensure clean state
    configure_logging()
    yield
    # Clear context after test
    from structlog.contextvars import clear_contextvars

    clear_contextvars()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
