"""Test JSON output format for production logging."""

import json

# Force JSON mode BEFORE importing logger
import os
import sys


os.environ["LOG_FORMAT"] = "json"
os.environ["LOG_LEVEL"] = "INFO"

from structlog.contextvars import bind_contextvars
from utils.logger import get_logger


logger = get_logger("test")

# Test 1: Simple log
logger.info("test_simple", key="value", number=42)

# Test 2: With context
bind_contextvars(user_id=123, session="abc")
logger.info("test_context", action="login")

# Test 3: With error (no exception for cleaner output)
logger.error("test_error", code=500, message="Server error")

print("\n--- VALIDATION ---")
print("✓ If logs above are JSON format, validation passed")
print("✓ Each line should be valid JSON with 'event', 'timestamp', 'level' fields")
