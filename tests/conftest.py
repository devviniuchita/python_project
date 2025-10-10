"""
Pytest configuration and shared fixtures.
"""

from typing import List
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def sample_documents() -> List[str]:
    """Sample documents for testing."""
    return [
        "O Perceptron é a base fundamental para o desenvolvimento de redes neurais mais complexas.",
        "O Perceptron é a forma mais elementar de uma rede neural.",
        "O Perceptron pode ser representado matematicamente como y=σ(w1x1 +w2x2).",
        "Em Python, as entradas e os pesos são representados por vetores e matrizes.",
        "O Perceptron é um classificador binário de problemas linearmente separáveis.",
        "O Perceptron individualmente não é capaz de resolver muitos problemas.",
        "A função de ativação do Perceptron é geralmente a função degrau.",
        "O algoritmo de aprendizado do Perceptron ajusta os pesos iterativamente.",
        "O Perceptron foi proposto por Frank Rosenblatt em 1957.",
        "O Perceptron multicamadas pode resolver problemas não linearmente separáveis.",
    ]


@pytest.fixture
def sample_query() -> str:
    """Sample query for testing."""
    return "Quais as limitações do Perceptron?"


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = MagicMock()
    settings.reranker_enabled = True
    settings.reranker_model = "BAAI/bge-reranker-base"
    settings.reranker_top_n = 5
    settings.reranker_score_threshold = 0.0
    return settings


@pytest.fixture
def mock_reranker():
    """Mock BGE Reranker for testing without loading actual model."""
    reranker = MagicMock()
    reranker.top_n = 5

    # Mock compress_documents to return top N documents
    def mock_compress(documents, query):
        return documents[: reranker.top_n]

    reranker.compress_documents = mock_compress
    return reranker
