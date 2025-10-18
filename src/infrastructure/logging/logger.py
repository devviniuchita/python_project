"""
Structured logging configuration using structlog.

This module provides:
- JSON logging for production (machine-parseable)
- Pretty console logging for development (human-readable)
- Context variables for request/operation tracking
- Performance-optimized configuration
- Environment-based log level and format control

Example:
    >>> from utils.logger import get_logger, configure_logging
    >>> configure_logging()
    >>> logger = get_logger(__name__)
    >>> logger.info("operation_started", user_id=123, query="test")
"""

import logging
import sys

from typing import Optional

import structlog

from src.infrastructure.config.settings import settings


# Try to use orjson for 2-3x faster JSON rendering
try:
    import orjson

    def orjson_serializer(obj, **kwargs):
        """Orjson serializer that returns str (not bytes)."""
        return orjson.dumps(obj).decode("utf-8")

    json_renderer = structlog.processors.JSONRenderer(serializer=orjson_serializer)
except ImportError:
    # Fallback to standard JSON
    json_renderer = structlog.processors.JSONRenderer()


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """
    Get a configured structlog logger instance.

    Args:
        name: Logger name (typically __name__ for module-specific loggers).
              If None, returns the root logger.

    Returns:
        BoundLogger: Configured structlog logger with all processors applied.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("user_logged_in", user_id=42, session="abc123")
        {"event": "user_logged_in", "user_id": 42, "session": "abc123", ...}
    """
    return structlog.get_logger(name)


def configure_logging() -> None:
    """
    Configure structlog based on environment settings.

    Configuration based on:
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR (from settings)
    - LOG_FORMAT: auto, json, console (from settings)
    - Terminal detection: Pretty console if TTY, JSON otherwise

    Processors applied:
    1. merge_contextvars: Include bound context variables
    2. add_log_level: Add "level" field (info, warning, error, etc.)
    3. format_exc_info: Format exceptions as structured data
    4. TimeStamper: Add ISO8601 UTC timestamp
    5. CallsiteParameterAdder: Add filename, function, line number
    6. JSONRenderer or ConsoleRenderer: Final output format

    Performance optimizations:
    - cache_logger_on_first_use: Skip repeated lookups (10-20% faster)
    - make_filtering_bound_logger: Early log level filtering
    - orjson serializer: 2-3x faster JSON rendering (if available)

    Example:
        >>> configure_logging()
        >>> logger = get_logger()
        >>> logger.info("system_started")
    """
    # Shared processors (always applied)
    shared_processors = [
        # Include context variables (query, user_id, etc.)
        structlog.contextvars.merge_contextvars,
        # Add log level field
        structlog.processors.add_log_level,
        # Format exceptions as structured data
        structlog.processors.format_exc_info,
        # Add ISO8601 UTC timestamp
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        # Add callsite info (filename, function, line) for debugging
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
    ]

    # Determine output format based on settings and environment
    log_format_lower = settings.log_format.lower()

    if log_format_lower == "json":
        # Force JSON output (production mode)
        processors = shared_processors + [json_renderer]
    elif log_format_lower == "console":
        # Force pretty console output (development mode)
        processors = shared_processors + [structlog.dev.ConsoleRenderer(colors=True)]
    else:  # auto (default)
        # Auto-detect: TTY = console, pipe/file = JSON
        if sys.stderr.isatty():
            processors = shared_processors + [
                structlog.dev.ConsoleRenderer(colors=True)
            ]
        else:
            processors = shared_processors + [json_renderer]

    # Parse log level from settings
    try:
        log_level = getattr(logging, settings.log_level.upper())
    except AttributeError:
        # Fallback to INFO if invalid level
        log_level = logging.INFO
        print(
            f"[LOGGER] Invalid LOG_LEVEL '{settings.log_level}', using INFO",
            file=sys.stderr,
        )

    # Configure structlog
    structlog.configure(
        # Cache loggers for performance (10-20% faster)
        cache_logger_on_first_use=True,
        # Early filtering by log level (skip processing if log level too low)
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        # Processor chain
        processors=processors,
        # Output to stdout (modern cloud/container practice)
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )

    # Log configuration info
    logger = get_logger(__name__)
    logger.debug(
        "logging_configured",
        log_level=settings.log_level,
        log_format=settings.log_format,
        is_tty=sys.stderr.isatty(),
    )


# Auto-configure on import if not already configured
# This allows "from utils.logger import get_logger" to just work
if not structlog.is_configured():
    configure_logging()
