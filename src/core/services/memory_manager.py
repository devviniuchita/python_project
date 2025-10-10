"""
Memory Management for Conversational RAG
Handles session management and conversation persistence
"""

import uuid

from typing import Dict

from langgraph.checkpoint.memory import MemorySaver


class ConversationManager:
    """
    Manages conversation sessions and memory.

    Features:
    - Session tracking with unique thread IDs
    - Memory persistence across turns
    - Conversation history management
    """

    def __init__(self):
        """Initialize conversation manager with memory saver."""
        self.memory = MemorySaver()
        self.active_sessions: Dict[str, str] = {}  # user_id -> thread_id mapping

    def get_or_create_session(self, user_id: str = "default") -> str:
        """
        Get existing session or create new one for user.

        Args:
            user_id: Unique identifier for user

        Returns:
            thread_id: UUID string for session tracking
        """
        if user_id not in self.active_sessions:
            thread_id = str(uuid.uuid4())
            self.active_sessions[user_id] = thread_id
            print(f"[SESSION] Created new session: {thread_id} for user: {user_id}")
            return thread_id

        thread_id = self.active_sessions[user_id]
        print(f"[SESSION] Using existing session: {thread_id} for user: {user_id}")
        return thread_id

    def reset_session(self, user_id: str = "default") -> str:
        """
        Reset session for user (start new conversation).

        Args:
            user_id: Unique identifier for user

        Returns:
            thread_id: New UUID string for session tracking
        """
        thread_id = str(uuid.uuid4())
        self.active_sessions[user_id] = thread_id
        print(f"[SESSION] Reset session: {thread_id} for user: {user_id}")
        return thread_id

    def get_config(self, user_id: str = "default") -> dict:
        """
        Get configuration dict for LangGraph execution.

        Args:
            user_id: Unique identifier for user

        Returns:
            Configuration dict with thread_id
        """
        thread_id = self.get_or_create_session(user_id)
        return {"configurable": {"thread_id": thread_id}}

    def get_memory(self) -> MemorySaver:
        """
        Get the memory saver instance.

        Returns:
            MemorySaver instance for graph compilation
        """
        return self.memory


# Global conversation manager instance
conversation_manager = ConversationManager()


def get_conversation_config(user_id: str = "default") -> dict:
    """
    Helper function to get conversation config.

    Args:
        user_id: Unique identifier for user

    Returns:
        Configuration dict for LangGraph
    """
    return conversation_manager.get_config(user_id)


def reset_conversation(user_id: str = "default") -> None:
    """
    Helper function to reset conversation.

    Args:
        user_id: Unique identifier for user
    """
    conversation_manager.reset_session(user_id)
    print(f"[MEMORY] Conversation reset for user: {user_id}")


def get_memory_saver() -> MemorySaver:
    """
    Helper function to get memory saver.

    Returns:
        MemorySaver instance
    """
    return conversation_manager.get_memory()
