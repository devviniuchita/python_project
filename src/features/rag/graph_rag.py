"""
LangGraph RAG System
Assembles the stateful graph workflow with nodes and conditional edges
"""

from typing import Any, Protocol, cast

from langgraph.graph import END, START, StateGraph

from src.core.domain.state import RAGState
from src.features.rag.nodes import (
    classify_question,
    generate_answer,
    refine_answer,
    rerank_documents,
    retrieve_adaptive,
    validate_quality,
)

# Maximum refinement iterations to prevent infinite loops
MAX_ITERATIONS = 2


class RAGGraphRunner(Protocol):
    """Protocol representing the compiled LangGraph executor."""

    def invoke(
        self, state: RAGState, config: Any | None = None
    ) -> dict[str, object]: ...


def should_refine(state: RAGState) -> str:
    """
    Conditional edge function to determine if answer needs refinement.

    Returns:
        END: If quality is good (>=0.7) or max iterations reached
        "refine": If answer needs improvement and iterations < MAX
    """
    quality_score = state["quality_score"]
    iterations = state["iterations"]

    # Good quality - stop here
    if quality_score >= 0.7:
        print(f"[DECISION] Quality good ({quality_score:.2f}) - ENDING")
        return str(END)

    # Max iterations reached - stop to prevent infinite loop
    if iterations >= MAX_ITERATIONS:
        print(f"[DECISION] Max iterations ({MAX_ITERATIONS}) reached - ENDING")
        return str(END)

    # Needs refinement
    print(
        f"[DECISION] Quality low ({quality_score:.2f}) - REFINING (iteration {iterations + 1})"
    )
    return "refine"


def create_rag_graph() -> RAGGraphRunner:
    """
    Creates and compiles the RAG workflow graph.

    Graph flow:
    START → classify → retrieve → generate → validate → [refine or END]
                                                            ↓
                                                        validate (loop)

    Returns:
        Compiled LangGraph StateGraph
    """
    # Initialize graph with state schema
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("classify", classify_question)
    workflow.add_node("retrieve", retrieve_adaptive)
    workflow.add_node("rerank", rerank_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("validate", validate_quality)
    workflow.add_node("refine", refine_answer)

    # Add edges - define flow
    workflow.add_edge(START, "classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "rerank")
    workflow.add_edge("rerank", "generate")
    workflow.add_edge("generate", "validate")

    # Conditional edge - decide to refine or end
    workflow.add_conditional_edges(
        "validate", should_refine, {"refine": "refine", END: END}
    )

    # After refinement, validate again
    workflow.add_edge("refine", "validate")

    # Compile graph
    graph = workflow.compile()

    print("[GRAPH] RAG workflow compiled successfully")
    return cast(RAGGraphRunner, graph)


def run_rag_query(question: str) -> str:
    """
    Executes RAG query through the LangGraph workflow.

    Args:
        question: User question to answer

    Returns:
        Generated answer string
    """
    graph = create_rag_graph()

    # Initialize state
    initial_state: RAGState = {
        "question": question,
        "complexity": "simple",
        "documents": [],
        "generation": "",
        "quality_score": 0.0,
        "iterations": 0,
    }

    print(f"\n{'='*60}")
    print(f"[QUERY] Starting RAG workflow for: {question}")
    print(f"{'='*60}\n")

    # Run graph
    final_state = cast(RAGState, graph.invoke(initial_state))

    # Extract results
    answer = final_state["generation"]
    quality = final_state["quality_score"]
    iterations = final_state["iterations"]
    complexity = final_state["complexity"]

    print(f"\n{'='*60}")
    print("[COMPLETE] Workflow finished")
    print(f"  - Complexity: {complexity}")
    print(f"  - Quality Score: {quality:.2f}")
    print(f"  - Refinement Iterations: {iterations}")
    print(f"  - Answer Length: {len(answer)} characters")
    print(f"{'='*60}\n")

    return answer


if __name__ == "__main__":
    # Test with sample question
    test_question = "Quais as limitações do Perceptron?"
    answer = run_rag_query(test_question)
    print(f"\n[ANSWER]\n{answer}")
