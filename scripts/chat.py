"""
Conversational RAG CLI
Interactive command-line interface for multi-turn conversations
"""

import os
import sys

from conversation_graph import run_conversational_query
from dotenv import load_dotenv
from memory_manager import get_conversation_config, reset_conversation

# Load environment
venv_env_path = "c:/Users/ADMIN/Desktop/rules-base/.venv/.env"
if os.path.exists(venv_env_path):
    load_dotenv(venv_env_path)


def print_header():
    """Print welcome header."""
    print("\n" + "=" * 80)
    print(" " * 20 + "🤖 CONVERSATIONAL RAG SYSTEM 🤖")
    print("=" * 80)
    print("💬 Multi-turn conversation with memory")
    print("🧠 Context-aware follow-up detection")
    print("🎯 Adaptive retrieval based on complexity")
    print("✨ Quality validation and refinement")
    print("=" * 80)
    print("\nCommands:")
    print("  - Type your question to chat")
    print("  - '/reset' - Start new conversation")
    print("  - '/quit' or '/exit' - Exit the system")
    print("  - '/help' - Show this help message")
    print("=" * 80 + "\n")


def print_help():
    """Print help message."""
    print("\n" + "-" * 80)
    print("📚 HELP - Available Commands:")
    print("-" * 80)
    print("  /reset    - Reset conversation history (start fresh)")
    print("  /quit     - Exit the conversational system")
    print("  /exit     - Exit the conversational system")
    print("  /help     - Show this help message")
    print("-" * 80 + "\n")


def run_interactive_conversation(user_id: str = "cli_user"):
    """
    Run interactive multi-turn conversation.

    Args:
        user_id: Unique identifier for user session
    """
    print_header()

    # Get initial config
    config = get_conversation_config(user_id)

    conversation_count = 0

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()

                if command in ["/quit", "/exit"]:
                    print("\n👋 Goodbye! Thank you for using Conversational RAG.")
                    print("=" * 80 + "\n")
                    break

                elif command == "/reset":
                    reset_conversation(user_id)
                    config = get_conversation_config(user_id)
                    conversation_count = 0
                    print("\n🔄 Conversation reset! Starting fresh conversation.\n")
                    continue

                elif command == "/help":
                    print_help()
                    continue

                else:
                    print(
                        f"\n❌ Unknown command: {user_input}. Type '/help' for available commands.\n"
                    )
                    continue

            # Process question
            conversation_count += 1
            print(f"\n[Turn {conversation_count}] Processing...\n")

            # Run conversational query
            answer = run_conversational_query(user_input, user_id, config)

            # Print answer
            print(f"\n{'='*80}")
            print("Assistant:")
            print("-" * 80)
            print(answer)
            print("=" * 80 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Use '/quit' to exit gracefully.")
            print("=" * 80 + "\n")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type '/quit' to exit.\n")
            continue


if __name__ == "__main__":
    # Check if user wants help
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print_help()
        sys.exit(0)

    # Run interactive conversation
    run_interactive_conversation()
