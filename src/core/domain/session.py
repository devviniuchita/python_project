"""Session configuration model with Pydantic validation.

This module provides validated configuration for conversation sessions,
ensuring type safety and data integrity for memory management.
"""

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ValidationInfo
from pydantic import field_validator


class SessionConfig(BaseModel):
    """Validated configuration for conversation sessions.

    This model ensures that session configurations are valid and immutable
    after creation, preventing accidental modifications that could corrupt
    conversation state.

    Attributes:
        thread_id: Unique UUID for conversation thread tracking
        max_turns: Maximum number of turns in session (must be >= 1)
        memory_window: Conversation context window size (1 <= x <= max_turns)

    Example:
        >>> from uuid import uuid4
        >>> config = SessionConfig(
        ...     thread_id=uuid4(),
        ...     max_turns=10,
        ...     memory_window=6
        ... )
        >>> print(config.max_turns)
        10
        >>> config.max_turns = 20  # Raises ValidationError (frozen)
    """

    thread_id: UUID = Field(
        ..., description="Unique UUID for conversation thread tracking"
    )

    max_turns: int = Field(
        default=10, ge=1, description="Maximum number of turns in session"
    )

    memory_window: int = Field(
        default=6, ge=1, le=20, description="Conversation context window size"
    )

    model_config = ConfigDict(
        frozen=True,  # Immutable after creation
        validate_assignment=True,  # Validate if assignment attempted
        str_strip_whitespace=True,  # Clean string inputs
        arbitrary_types_allowed=False,  # Only allow standard types
    )

    @field_validator('memory_window')
    @classmethod
    def validate_memory_window(cls, v: int, info: ValidationInfo) -> int:
        """Ensure memory_window doesn't exceed max_turns.

        Args:
            v: The memory_window value to validate
            info: Validation context with access to other fields

        Returns:
            The validated memory_window value

        Raises:
            ValueError: If memory_window > max_turns
        """
        max_turns = info.data.get('max_turns', 10)
        if v > max_turns:
            raise ValueError(
                f"memory_window ({v}) cannot exceed max_turns ({max_turns})"
            )
        return v
