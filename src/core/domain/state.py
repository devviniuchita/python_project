"""
State definitions for RAG system using LangGraph.

Note: TypedDict is used instead of Pydantic BaseModel for performance.
Type hints with Literal and Field provide static type checking without
runtime validation overhead (~2.5x faster than BaseModel).
"""

from typing import Annotated
from typing import List
from typing import Literal
from typing import Sequence
from typing import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import Field


class RAGState(TypedDict):
    """
    Represents the state of the RAG graph workflow.

    Attributes:
        question: Original user question
        complexity: Classification as "simple" or "complex" (Literal type-safe enum)
        documents: List of retrieved documents
        generation: LLM generated answer
        quality_score: Validation score (0.0-1.0 range, higher is better)
        iterations: Number of refinement iterations performed (non-negative)

    Note:
        Field constraints (ge, le) provide documentation and static type checking
        but do NOT perform runtime validation (TypedDict performance benefit).
    """

    question: str
    complexity: Literal["simple", "complex"]  # Type-safe enum (only these values)
    documents: List[str]
    generation: str
    quality_score: Annotated[float, Field(ge=0.0, le=1.0)]  # Range 0.0-1.0
    iterations: Annotated[int, Field(ge=0)]  # Non-negative integer


class ConversationalRAGState(TypedDict):
    """
    Extended state for conversational RAG with memory.

    Attributes:
        messages: Chat history using LangChain message format (with add_messages reducer)
        question: Current/expanded user question
        complexity: Classification as "simple" or "complex" (Literal type-safe enum)
        documents: List of retrieved documents
        generation: LLM generated answer
        quality_score: Validation score (0.0-1.0 range, higher is better)
        iterations: Number of refinement iterations performed (non-negative)
        is_followup: Whether question is a follow-up to previous message
        original_question: Raw user input before context expansion

    Note:
        Field constraints (ge, le) provide documentation and static type checking
        but do NOT perform runtime validation (TypedDict performance benefit).
        For runtime validation, use Pydantic BaseModel (not recommended for
        LangGraph hot path due to ~2.5x performance penalty).
    """

    # Chat history with add_messages reducer for automatic appending
    messages: Annotated[Sequence[BaseMessage], add_messages]
    question: str
    complexity: Literal["simple", "complex"]  # Type-safe enum (only these values)
    documents: List[str]
    generation: str
    quality_score: Annotated[float, Field(ge=0.0, le=1.0)]  # Range 0.0-1.0
    iterations: Annotated[int, Field(ge=0)]  # Non-negative integer
    is_followup: bool
    original_question: str
