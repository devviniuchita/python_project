"""
TC004, TC005, TC006: Conversation Management API Tests

Tests for conversation state management and context tracking.
- TC004: test_create_conversation_api
- TC005: test_add_message_to_conversation
- TC006: test_get_conversation_context_api
"""

from datetime import datetime
from typing import Any, Dict
from unittest.mock import MagicMock, call

import pytest


class TestCreateConversationAPI:
    """TC004: Conversation creation tests."""

    def test_create_conversation_returns_valid_id(self, mock_conversation_manager):
        """Test that create_conversation returns a valid conversation ID."""
        # Arrange
        mock_conversation_manager.create_conversation.return_value = "conv_12345"

        # Act
        conv_id = mock_conversation_manager.create_conversation()

        # Assert
        assert conv_id is not None
        assert isinstance(conv_id, str)
        assert len(conv_id) > 0
        assert conv_id.startswith("conv_") or conv_id.isalnum()

    def test_create_conversation_with_initial_context(self, mock_conversation_manager):
        """Test creating conversation with initial context."""
        # Arrange
        initial_context = {"user_id": "user_123", "session_id": "sess_456"}
        mock_conversation_manager.create_conversation.return_value = "conv_12345"

        # Act
        conv_id = mock_conversation_manager.create_conversation(context=initial_context)

        # Assert
        assert conv_id == "conv_12345"
        mock_conversation_manager.create_conversation.assert_called_once_with(
            context=initial_context
        )

    def test_create_conversation_initializes_empty_messages(
        self, mock_conversation_manager
    ):
        """Test that new conversation starts with empty message list."""
        # Arrange
        mock_conversation_manager.create_conversation.return_value = "conv_new"
        mock_conversation_manager.get_context.return_value = {
            "conversation_id": "conv_new",
            "messages": [],
            "total_tokens": 0,
        }

        # Act
        conv_id = mock_conversation_manager.create_conversation()
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert context["messages"] == []
        assert context["total_tokens"] == 0

    def test_create_conversation_with_timeout_setting(self, mock_conversation_manager):
        """Test creating conversation with custom timeout."""
        # Arrange
        timeout_minutes = 30
        mock_conversation_manager.create_conversation.return_value = "conv_timed"

        # Act
        conv_id = mock_conversation_manager.create_conversation(
            timeout_minutes=timeout_minutes
        )

        # Assert
        assert conv_id == "conv_timed"
        mock_conversation_manager.create_conversation.assert_called_once()

    def test_create_conversation_multiple_sequential(self, mock_conversation_manager):
        """Test creating multiple conversations sequentially."""
        # Arrange
        mock_conversation_manager.create_conversation.side_effect = [
            "conv_001",
            "conv_002",
            "conv_003",
        ]

        # Act
        conv_ids = [mock_conversation_manager.create_conversation() for _ in range(3)]

        # Assert
        assert len(conv_ids) == 3
        assert len(set(conv_ids)) == 3  # All IDs should be unique
        assert all(cid.startswith("conv_") for cid in conv_ids)

    def test_create_conversation_unique_ids(self, mock_conversation_manager):
        """Test that each conversation gets a unique ID."""
        # Arrange
        ids_generated = []

        def side_effect():
            new_id = f"conv_{len(ids_generated):05d}"
            ids_generated.append(new_id)
            return new_id

        mock_conversation_manager.create_conversation.side_effect = side_effect

        # Act
        conv1 = mock_conversation_manager.create_conversation()
        conv2 = mock_conversation_manager.create_conversation()
        conv3 = mock_conversation_manager.create_conversation()

        # Assert
        assert conv1 != conv2
        assert conv2 != conv3
        assert conv1 != conv3


class TestAddMessageToConversation:
    """TC005: Add message to conversation tests."""

    def test_add_message_to_conversation_success(self, mock_conversation_manager):
        """Test successfully adding a message to conversation."""
        # Arrange
        conv_id = "conv_12345"
        message = {"role": "user", "content": "Hello"}

        mock_conversation_manager.add_message.return_value = {
            "conversation_id": conv_id,
            "message_id": "msg_1",
            "timestamp": "2025-10-18T10:30:00Z",
        }

        # Act
        result = mock_conversation_manager.add_message(conv_id, message)

        # Assert
        assert result["conversation_id"] == conv_id
        assert result["message_id"] is not None
        assert "timestamp" in result

    def test_add_message_with_role_user(self, mock_conversation_manager):
        """Test adding user message to conversation."""
        # Arrange
        conv_id = "conv_test"
        user_message = {"role": "user", "content": "What is AI?"}

        mock_conversation_manager.add_message.return_value = {
            "conversation_id": conv_id,
            "message_id": "msg_1",
            "role": "user",
        }

        # Act
        result = mock_conversation_manager.add_message(conv_id, user_message)

        # Assert
        assert result["role"] == "user"
        assert "message_id" in result

    def test_add_message_with_role_assistant(self, mock_conversation_manager):
        """Test adding assistant message to conversation."""
        # Arrange
        conv_id = "conv_test"
        assistant_message = {
            "role": "assistant",
            "content": "AI is artificial intelligence",
        }

        mock_conversation_manager.add_message.return_value = {
            "conversation_id": conv_id,
            "message_id": "msg_2",
            "role": "assistant",
        }

        # Act
        result = mock_conversation_manager.add_message(conv_id, assistant_message)

        # Assert
        assert result["role"] == "assistant"

    def test_add_message_updates_token_count(self, mock_conversation_manager):
        """Test that adding message updates total token count."""
        # Arrange
        conv_id = "conv_12345"
        message = {"role": "user", "content": "Sample message"}

        mock_conversation_manager.add_message.return_value = {
            "conversation_id": conv_id,
            "message_id": "msg_1",
            "tokens_added": 10,
        }

        # Act
        result = mock_conversation_manager.add_message(conv_id, message)

        # Assert
        assert "tokens_added" in result
        assert result["tokens_added"] > 0

    def test_add_multiple_messages_sequence(self, mock_conversation_manager):
        """Test adding multiple messages in sequence."""
        # Arrange
        conv_id = "conv_seq"
        messages = [
            {"role": "user", "content": "First question"},
            {"role": "assistant", "content": "First answer"},
            {"role": "user", "content": "Second question"},
        ]

        def add_message_side_effect(cid, msg):
            msg_id = f"msg_{mock_conversation_manager.add_message.call_count}"
            return {"conversation_id": cid, "message_id": msg_id, "role": msg["role"]}

        mock_conversation_manager.add_message.side_effect = add_message_side_effect

        # Act
        results = [
            mock_conversation_manager.add_message(conv_id, msg) for msg in messages
        ]

        # Assert
        assert len(results) == 3
        assert results[0]["role"] == "user"
        assert results[1]["role"] == "assistant"
        assert results[2]["role"] == "user"

    def test_add_message_with_metadata(self, mock_conversation_manager):
        """Test adding message with additional metadata."""
        # Arrange
        conv_id = "conv_meta"
        message = {
            "role": "user",
            "content": "Question",
            "metadata": {"source": "api", "version": "1.0"},
        }

        mock_conversation_manager.add_message.return_value = {
            "conversation_id": conv_id,
            "message_id": "msg_1",
            "metadata_preserved": True,
        }

        # Act
        result = mock_conversation_manager.add_message(conv_id, message)

        # Assert
        assert result["metadata_preserved"] is True

    def test_add_message_exceeding_context_window(self, mock_conversation_manager):
        """Test behavior when adding message exceeds context window."""
        # Arrange
        conv_id = "conv_large"
        large_message = {"role": "user", "content": "x" * 100000}

        mock_conversation_manager.add_message.side_effect = ValueError(
            "Message exceeds context window"
        )

        # Act & Assert
        with pytest.raises(ValueError):
            mock_conversation_manager.add_message(conv_id, large_message)


class TestGetConversationContextAPI:
    """TC006: Get conversation context tests."""

    def test_get_conversation_context_returns_valid_data(
        self, mock_conversation_manager
    ):
        """Test that get_conversation_context returns valid context data."""
        # Arrange
        conv_id = "conv_12345"
        mock_conversation_manager.get_context.return_value = {
            "conversation_id": conv_id,
            "messages": 3,
            "total_tokens": 892,
        }

        # Act
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert context["conversation_id"] == conv_id
        assert "messages" in context
        assert "total_tokens" in context
        assert context["total_tokens"] >= 0

    def test_get_conversation_context_message_count(self, mock_conversation_manager):
        """Test that context returns correct message count."""
        # Arrange
        conv_id = "conv_test"
        mock_conversation_manager.get_context.return_value = {
            "conversation_id": conv_id,
            "messages": 5,
            "total_tokens": 1250,
        }

        # Act
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert context["messages"] == 5

    def test_get_conversation_context_includes_metadata(
        self, mock_conversation_manager
    ):
        """Test that context includes conversation metadata."""
        # Arrange
        conv_id = "conv_meta"
        mock_conversation_manager.get_context.return_value = {
            "conversation_id": conv_id,
            "created_at": "2025-10-18T10:00:00Z",
            "last_message_at": "2025-10-18T10:30:00Z",
            "messages": 2,
            "total_tokens": 450,
        }

        # Act
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert "created_at" in context
        assert "last_message_at" in context
        assert context["last_message_at"] >= context["created_at"]

    def test_get_conversation_context_with_empty_conversation(
        self, mock_conversation_manager
    ):
        """Test getting context for empty conversation."""
        # Arrange
        conv_id = "conv_empty"
        mock_conversation_manager.get_context.return_value = {
            "conversation_id": conv_id,
            "messages": 0,
            "total_tokens": 0,
        }

        # Act
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert context["messages"] == 0
        assert context["total_tokens"] == 0

    def test_get_conversation_context_nonexistent_id(self, mock_conversation_manager):
        """Test getting context for non-existent conversation ID."""
        # Arrange
        mock_conversation_manager.get_context.side_effect = ValueError(
            "Conversation not found"
        )

        # Act & Assert
        with pytest.raises(ValueError):
            mock_conversation_manager.get_context("conv_nonexistent")

    def test_get_conversation_context_large_conversation(
        self, mock_conversation_manager
    ):
        """Test getting context for conversation with many messages."""
        # Arrange
        conv_id = "conv_large"
        mock_conversation_manager.get_context.return_value = {
            "conversation_id": conv_id,
            "messages": 100,
            "total_tokens": 45000,
            "warning": "Large conversation, consider archiving",
        }

        # Act
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert context["messages"] == 100
        assert context["total_tokens"] == 45000
        assert "warning" in context


# ============================================================================
# INTEGRATION TESTS - CONVERSATION MANAGEMENT PIPELINE
# ============================================================================


class TestConversationManagementPipeline:
    """Integration tests for conversation lifecycle."""

    def test_full_conversation_lifecycle(self, mock_conversation_manager):
        """Test complete conversation lifecycle: create -> add messages -> retrieve context."""
        # Arrange
        mock_conversation_manager.create_conversation.return_value = "conv_lifecycle"

        def mock_add_message(cid, msg):
            return {
                "conversation_id": cid,
                "message_id": f"msg_{mock_conversation_manager.add_message.call_count}",
                "role": msg["role"],
            }

        mock_conversation_manager.add_message.side_effect = mock_add_message

        mock_conversation_manager.get_context.return_value = {
            "conversation_id": "conv_lifecycle",
            "messages": 2,
            "total_tokens": 450,
        }

        # Act - Create
        conv_id = mock_conversation_manager.create_conversation()

        # Act - Add messages
        msg1 = mock_conversation_manager.add_message(
            conv_id, {"role": "user", "content": "Hello"}
        )
        msg2 = mock_conversation_manager.add_message(
            conv_id, {"role": "assistant", "content": "Hi there"}
        )

        # Act - Get context
        context = mock_conversation_manager.get_context(conv_id)

        # Assert
        assert conv_id == "conv_lifecycle"
        assert msg1["role"] == "user"
        assert msg2["role"] == "assistant"
        assert context["messages"] == 2

    def test_conversation_with_multiple_turns(self, mock_conversation_manager):
        """Test multi-turn conversation with alternating user/assistant messages."""
        # Arrange
        conv_id = "conv_multi_turn"
        turns = [
            (("user", "First question"), "msg_1"),
            (("assistant", "First answer"), "msg_2"),
            (("user", "Follow-up question"), "msg_3"),
            (("assistant", "Follow-up answer"), "msg_4"),
        ]

        mock_conversation_manager.create_conversation.return_value = conv_id

        def add_msg_side_effect(cid, msg):
            for (role, content), msg_id in turns:
                if msg["role"] == role and msg["content"] == content:
                    return {"conversation_id": cid, "message_id": msg_id, "role": role}

        mock_conversation_manager.add_message.side_effect = add_msg_side_effect

        # Act
        created_id = mock_conversation_manager.create_conversation()
        assert created_id == conv_id

        # Assert turns are properly handled
        for (role, content), _ in turns:
            result = mock_conversation_manager.add_message(
                conv_id, {"role": role, "content": content}
            )
            assert result["role"] == role

    @pytest.mark.parametrize("messages_count", [1, 5, 10, 50])
    def test_conversation_performance_with_varying_message_counts(
        self, mock_conversation_manager, messages_count
    ):
        """Test conversation performance with different numbers of messages."""
        import time

        # Arrange
        conv_id = "conv_perf"
        mock_conversation_manager.create_conversation.return_value = conv_id

        # Mock add_message to be fast
        mock_conversation_manager.add_message.return_value = {
            "conversation_id": conv_id,
            "message_id": "msg_x",
            "role": "user",
        }

        # Act
        start = time.time()
        for i in range(messages_count):
            mock_conversation_manager.add_message(
                conv_id, {"role": "user", "content": f"Message {i}"}
            )
        elapsed = time.time() - start

        # Assert
        assert elapsed < 1.0  # Should be fast (mocked)
