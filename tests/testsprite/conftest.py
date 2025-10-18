"""
Shared pytest fixtures for TestSprite RAG system tests.

Provides reusable fixtures for document retrieval, LLM mocking, conversation
state management, and test data generation.
"""

from typing import Any
from typing import Dict
from typing import List
from unittest.mock import MagicMock
from unittest.mock import patch

import numpy as np
import pytest


# ============================================================================
# DOCUMENT & RETRIEVAL FIXTURES
# ============================================================================


@pytest.fixture
def sample_documents() -> List[str]:
    """Sample documents for retrieval testing."""
    return [
        "O Perceptron é o modelo de rede neural mais simples e fundamental.",
        "O Perceptron utiliza uma função de ativação linear para classificação binária.",
        "Redes neurais profundas são compostas por múltiplas camadas de neurônios.",
        "Backpropagation é o algoritmo essencial para treinamento de redes neurais.",
        "O aprendizado de máquina requer grandes volumes de dados para treinamento eficaz.",
        "Modelos de linguagem utilizam transformers para processar sequências de texto.",
        "Embeddings são representações vetoriais de texto em espaço multidimensional.",
        "Busca semântica usa embeddings para encontrar documentos similares ao query.",
    ]


@pytest.fixture
def sample_query() -> str:
    """Sample query for retrieval testing."""
    return "Como funciona o Perceptron em redes neurais?"


@pytest.fixture
def mock_embeddings():
    """Mock embeddings model."""
    mock = MagicMock()
    # Return random embeddings of dimension 768 (standard BERT/BGE size)
    mock.embed.side_effect = lambda text: np.random.randn(768).tolist()

    # Return one embedding per document passed to embed_documents
    def _embed_documents(docs):
        # Ensure docs is iterable and produce one embedding per item
        try:
            return [np.random.randn(768).tolist() for _ in docs]
        except TypeError:
            # If a single string was passed, return a single embedding
            return [np.random.randn(768).tolist()]

    mock.embed_documents.side_effect = _embed_documents
    return mock


@pytest.fixture
def mock_retriever(sample_documents):
    """Mock document retriever."""
    mock = MagicMock()
    mock.retrieve_documents.return_value = sample_documents[:3]  # Top 3 docs
    mock.get_similarity_scores.return_value = [0.95, 0.87, 0.76]
    return mock


@pytest.fixture
def mock_reranker():
    """Mock document reranker."""
    mock = MagicMock()
    # Simulate reranking scores (typically between 0 and 1)
    mock.rerank_documents.return_value = {
        "documents": ["Doc 1", "Doc 2"],
        "scores": [0.92, 0.85],
        "indices": [0, 2],
    }
    mock.calculate_scores.return_value = np.array([0.95, 0.87, 0.76, 0.61, 0.54])
    return mock


# ============================================================================
# LLM & GENERATION FIXTURES
# ============================================================================


@pytest.fixture
def mock_llm():
    """Mock LLM for response generation."""
    mock = MagicMock()
    mock.generate.return_value = (
        "O Perceptron é um algoritmo de aprendizado supervisionado para "
        "classificação binária linear. Utiliza uma função de ativação linear "
        "e ajusta pesos através do algoritmo de aprendizado por correção de erros."
    )
    mock.generate_with_context.return_value = {
        "response": "Generated response text",
        "confidence": 0.87,
        "tokens_used": 45,
    }
    return mock


@pytest.fixture
def mock_conversation_manager():
    """Mock conversation state manager."""
    mock = MagicMock()
    mock.create_conversation.return_value = "conv_12345"
    mock.add_message.return_value = {
        "conversation_id": "conv_12345",
        "message_id": "msg_1",
        "timestamp": "2025-10-18T10:30:00Z",
    }
    mock.get_context.return_value = {
        "conversation_id": "conv_12345",
        "messages": 3,
        "total_tokens": 892,
    }
    return mock


# ============================================================================
# QUALITY & THRESHOLD FIXTURES
# ============================================================================


@pytest.fixture
def quality_validator():
    """Mock quality validation system."""
    mock = MagicMock()
    mock.validate_quality.return_value = {
        "passes_threshold": True,
        "score": 0.88,
        "threshold": 0.70,
    }
    mock.calculate_confidence.return_value = 0.87
    mock.apply_adaptive_threshold.return_value = {
        "original_scores": [0.95, 0.87, 0.76],
        "adjusted_scores": [0.90, 0.80, 0.65],
        "threshold": 0.75,
    }
    return mock


@pytest.fixture
def quality_metrics() -> Dict[str, float]:
    """Standard quality metrics for RAG system."""
    return {
        "retrieval_recall": 0.85,
        "retrieval_precision": 0.92,
        "answer_relevancy": 0.88,
        "context_relevancy": 0.87,
        "overall_quality": 0.88,
    }


# ============================================================================
# STATE & CONTEXT FIXTURES
# ============================================================================


@pytest.fixture
def rag_state() -> Dict[str, Any]:
    """RAG system state for integration tests."""
    return {
        "conversation_id": "test_conv_001",
        "messages": [
            {"role": "user", "content": "Sample question"},
            {"role": "assistant", "content": "Sample answer"},
        ],
        "context_window": 4096,
        "messages_count": 2,
        "total_tokens": 450,
    }


@pytest.fixture
def test_dataset() -> List[Dict[str, Any]]:
    """Test dataset with queries and expected contexts."""
    return [
        {
            "query": "O que é machine learning?",
            "expected_contexts": 3,
            "min_relevancy": 0.75,
        },
        {
            "query": "Como funcionam transformers?",
            "expected_contexts": 3,
            "min_relevancy": 0.80,
        },
        {
            "query": "Explique redes neurais convolucionais",
            "expected_contexts": 3,
            "min_relevancy": 0.78,
        },
    ]


# ============================================================================
# INTEGRATION FIXTURES
# ============================================================================


@pytest.fixture
def rag_system_mocks(
    mock_retriever, mock_reranker, mock_llm, mock_conversation_manager
):
    """Complete RAG system with all mocked components."""
    return {
        "retriever": mock_retriever,
        "reranker": mock_reranker,
        "llm": mock_llm,
        "conversation_manager": mock_conversation_manager,
    }


@pytest.fixture
def patched_rag_modules():
    """Provide patches for all RAG system modules."""
    patches = {
        "retriever": patch("src.features.retrieval.faiss_retriever"),
        "reranker": patch("src.features.reranking.reranker"),
        "llm": patch("src.features.generation.llm_provider"),
        "conversation": patch("src.features.conversation.conversation_graph"),
    }
    return patches


# ============================================================================
# PARAMETRIZATION FIXTURES
# ============================================================================


@pytest.fixture(
    params=[
        {"threshold": 0.5, "expected_results": 5},
        {"threshold": 0.7, "expected_results": 3},
        {"threshold": 0.9, "expected_results": 1},
    ]
)
def threshold_params(request):
    """Parametrized thresholds for testing adaptive filtering."""
    return request.param


@pytest.fixture(params=["gpt-4", "claude-3", "open-source"])
def llm_model_variants(request):
    """Different LLM model variants for compatibility testing."""
    return request.param


# ============================================================================
# CLEANUP & UTILITY FIXTURES
# ============================================================================


@pytest.fixture
def reset_state():
    """Reset system state after test."""
    yield
    # Cleanup code here
    pass


@pytest.fixture
def capture_logs(caplog):
    """Capture and analyze system logs."""
    return caplog
