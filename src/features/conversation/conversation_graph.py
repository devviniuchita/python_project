"""
Conversational RAG Graph with Memory
Integrates chat history, context analysis, and follow-up handling
"""

from typing import Any, Protocol, cast

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from src.core.domain.state import ConversationalRAGState
from src.core.services.memory_manager import get_conversation_config, get_memory_saver
from src.features.conversation import (
    analyze_context,
    check_clarification,
    expand_question,
)
from src.features.rag.nodes import (
    classify_question,
    generate_answer,
    refine_answer,
    rerank_documents,
    retrieve_adaptive,
    validate_quality,
)

# Maximum refinement iterations
MAX_ITERATIONS = 2


class ConversationalGraphRunner(Protocol):
    """Protocol for the conversational graph executor."""

    def invoke(
        self, state: ConversationalRAGState, config: Any | None = None
    ) -> dict[str, object]: ...


def should_refine(state: ConversationalRAGState) -> str:
    """
    Conditional edge to determine if answer needs refinement.

    Returns:
        END: If quality is good (>=0.7) or max iterations reached
        "refine": If answer needs improvement
    """
    quality_score = state["quality_score"]
    iterations = state["iterations"]

    if quality_score >= 0.7:
        print(f"[DECISION] Quality good ({quality_score:.2f}) - ENDING")
        return str(END)

    if iterations >= MAX_ITERATIONS:
        print(f"[DECISION] Max iterations ({MAX_ITERATIONS}) reached - ENDING")
        return str(END)

    print(
        f"[DECISION] Quality low ({quality_score:.2f}) - REFINING (iteration {iterations + 1})"
    )
    return "refine"


def should_proceed_or_clarify(state: ConversationalRAGState) -> str:
    """
    Conditional edge to check if we should proceed or ask for clarification.

    Returns:
        "classify": Proceed with normal flow
        END: If clarification question was generated
    """
    # If generation already set (clarification), end here
    # Using approximate comparison for float to avoid precision issues
    quality_score = state["quality_score"]
    if state["generation"] and abs(quality_score - 0.5) < 0.01:
        print("[DECISION] Clarification needed - ENDING for user response")
        return str(END)

    print("[DECISION] Question clear - PROCEEDING to classification")
    return "classify"


def create_conversational_rag_graph() -> ConversationalGraphRunner:
    """
    Creates and compiles the conversational RAG workflow graph with memory.

    Graph flow:
    START
      ↓
    analyze_context (detect follow-up)
      ↓
    expand_question (if follow-up)
      ↓
    check_clarification (if ambiguous)
      ↓
    [CONDITIONAL: clarify or proceed]
      ↓
    classify → retrieve → generate → validate → [refine or END]
                                                    ↓
                                                validate (loop)

    Returns:
        Compiled LangGraph StateGraph with memory
    """
    # Initialize graph with conversational state
    workflow = StateGraph(ConversationalRAGState)

    # Add conversational nodes
    workflow.add_node("analyze_context", analyze_context)
    workflow.add_node("expand_question", expand_question)
    workflow.add_node("check_clarification", check_clarification)

    # Add RAG nodes (reused from original system)
    workflow.add_node("classify", classify_question)
    workflow.add_node("retrieve", retrieve_adaptive)
    workflow.add_node("rerank", rerank_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("validate", validate_quality)
    workflow.add_node("refine", refine_answer)

    # Define flow
    workflow.add_edge(START, "analyze_context")
    workflow.add_edge("analyze_context", "expand_question")
    workflow.add_edge("expand_question", "check_clarification")

    # Conditional: proceed or ask clarification
    workflow.add_conditional_edges(
        "check_clarification",
        should_proceed_or_clarify,
        {"classify": "classify", END: END},
    )

    # Normal RAG flow
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "rerank")
    workflow.add_edge("rerank", "generate")
    workflow.add_edge("generate", "validate")

    # Conditional: refine or end
    workflow.add_conditional_edges(
        "validate", should_refine, {"refine": "refine", END: END}
    )

    # After refinement, validate again
    workflow.add_edge("refine", "validate")

    # Compile with memory
    memory = get_memory_saver()
    graph = workflow.compile(checkpointer=memory)

    print("[GRAPH] Conversational RAG workflow compiled successfully with memory")
    return cast(ConversationalGraphRunner, graph)


def run_conversational_query(
    question: str,
    user_id: str = "default",
    config: dict[str, Any] | None = None,
) -> str:
    """
    Executes conversational RAG query with memory.

    Args:
        question: User question
        user_id: Unique user identifier for session management
        config: Optional config dict (will create if None)

    Returns:
        Generated answer string
    """
    graph = create_conversational_rag_graph()

    # Get or create config
    if config is None:
        config = get_conversation_config(user_id)

    # Create initial state with human message
    initial_state: ConversationalRAGState = {
        "messages": [HumanMessage(content=question)],
        "question": question,
        "complexity": "simple",
        "documents": [],
        "generation": "",
        "quality_score": 0.0,
        "iterations": 0,
        "is_followup": False,
        "original_question": question,
    }

    print(f"\n{'='*60}")
    print(f"[QUERY] Starting conversational RAG for: {question}")
    print(f"[QUERY] User ID: {user_id}")
    print(f"[QUERY] Thread ID: {config['configurable']['thread_id']}")
    print(f"{'='*60}\n")

    # Run graph with memory
    final_state = cast(
        ConversationalRAGState,
        graph.invoke(initial_state, config),
    )

    # Extract results
    answer = final_state["generation"]
    quality = final_state["quality_score"]
    iterations = final_state["iterations"]
    complexity = final_state["complexity"]
    is_followup = final_state["is_followup"]

    print(f"\n{'='*60}")
    print("[COMPLETE] Workflow finished")
    print(f"  - Is Follow-up: {is_followup}")
    print(f"  - Complexity: {complexity}")
    print(f"  - Quality Score: {quality:.2f}")
    print(f"  - Refinement Iterations: {iterations}")
    print(f"  - Answer Length: {len(answer)} characters")
    print(f"{'='*60}\n")

    return answer
