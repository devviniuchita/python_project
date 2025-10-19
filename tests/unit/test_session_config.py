"""Test script to validate SessionConfig Pydantic model."""

from typing import cast
from uuid import UUID, uuid4

from pydantic import ValidationError

from src.core.domain.session import SessionConfig

print("=" * 80)
print("SESSIONCONFIG PYDANTIC VALIDATION TESTS")
print("=" * 80)

# Test 1: Valid configuration
print("\n[Test 1] Valid SessionConfig:")
try:
    config = SessionConfig(thread_id=uuid4(), max_turns=10, memory_window=6)
    print("✅ PASS - SessionConfig created successfully")
    print(f"   thread_id: {config.thread_id}")
    print(f"   max_turns: {config.max_turns}")
    print(f"   memory_window: {config.memory_window}")
    print(f"   thread_id type: {type(config.thread_id).__name__}")
except Exception as e:
    print(f"❌ FAIL - {e}")

# Test 2: UUID auto-conversion from string
print("\n[Test 2] UUID auto-conversion from string:")
try:
    config = SessionConfig(
        thread_id=cast(UUID, "12345678-1234-1234-1234-123456789012"),
        max_turns=5,
    )
    print("✅ PASS - UUID converted from string")
    print("   Input: str")
    print(f"   Output: {type(config.thread_id).__name__}")
    print(f"   Value: {config.thread_id}")
except Exception as e:
    print(f"❌ FAIL - {e}")

# Test 3: Invalid max_turns (< 1)
print("\n[Test 3] Invalid max_turns (must be >= 1):")
try:
    config = SessionConfig(thread_id=uuid4(), max_turns=0)
    print("❌ FAIL - Should have raised ValidationError")
except ValidationError as e:
    print("✅ PASS - ValidationError raised as expected")
    print(f"   Error: {e.errors()[0]['msg']}")

# Test 4: memory_window > max_turns
print("\n[Test 4] memory_window exceeding max_turns:")
try:
    config = SessionConfig(thread_id=uuid4(), max_turns=5, memory_window=10)
    print("❌ FAIL - Should have raised ValidationError")
except ValidationError as e:
    print("✅ PASS - ValidationError raised as expected")
    print(f"   Error: {e.errors()[0]['msg']}")

# Test 5: Frozen immutability
print("\n[Test 5] Frozen immutability test:")
try:
    config = SessionConfig(thread_id=uuid4())
    original_max = config.max_turns
    config.max_turns = 20  # Should raise ValidationError
    print("❌ FAIL - Should have raised ValidationError for frozen field")
except ValidationError:
    print("✅ PASS - ValidationError raised for frozen instance")
    print("   Error: Instance is frozen")

# Test 6: Default values
print("\n[Test 6] Default values:")
try:
    config = SessionConfig(thread_id=uuid4())
    assert config.max_turns == 10, "Default max_turns should be 10"
    assert config.memory_window == 6, "Default memory_window should be 6"
    print("✅ PASS - Default values applied correctly")
    print(f"   max_turns: {config.max_turns} (default)")
    print(f"   memory_window: {config.memory_window} (default)")
except Exception as e:
    print(f"❌ FAIL - {e}")

# Test 7: Invalid UUID type
print("\n[Test 7] Invalid UUID type (integer):")
try:
    config = SessionConfig(thread_id=cast(UUID, 1234567812412341234567812345678))
    print("❌ FAIL - Should have raised ValidationError")
except ValidationError as e:
    print("✅ PASS - ValidationError raised as expected")
    print(f"   Error: {e.errors()[0]['type']}")

# Test 8: memory_window at upper bound
print("\n[Test 8] memory_window at upper bound (20):")
try:
    config = SessionConfig(thread_id=uuid4(), max_turns=25, memory_window=20)
    print("✅ PASS - memory_window=20 accepted (upper bound)")
    print(f"   max_turns: {config.max_turns}")
    print(f"   memory_window: {config.memory_window}")
except Exception as e:
    print(f"❌ FAIL - {e}")

# Test 9: memory_window exceeds upper bound
print("\n[Test 9] memory_window exceeds upper bound (>20):")
try:
    config = SessionConfig(thread_id=uuid4(), max_turns=30, memory_window=25)
    print("❌ FAIL - Should have raised ValidationError")
except ValidationError as e:
    print("✅ PASS - ValidationError raised as expected")
    print(f"   Error: {e.errors()[0]['msg']}")

print("\n" + "=" * 80)
print("VALIDATION TESTS COMPLETE!")
print("=" * 80)
