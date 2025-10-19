"""
LangGraph Nodes for RAG System
Each node is a function that receives state and returns updated state
"""

from typing import Literal

from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langsmith import traceable

from src.core.domain.state import RAGState
from src.features.reranking.reranker import rerank_documents as apply_reranking
from src.infrastructure.config.settings import settings

# Initialize components
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db_path = "banco_faiss"
llm = ChatGoogleGenerativeAI(model=settings.llm_model, temperature=0)


def _normalize_complexity(value: str) -> Literal["simple", "complex"]:
    """Normalize LLM output to the supported complexity literals."""
    normalized = value.strip().lower()
    if normalized.startswith("simp"):
        return "simple"
    if normalized.startswith("compl"):
        return "complex"
    # Prefer conservative default when uncertain to keep retrieval broad.
    return "complex"


@traceable(run_type="chain", name="Classify Question Complexity")
def classify_question(state: RAGState) -> RAGState:
    """
    Classifies question complexity as 'simple' or 'complex'.
    Simple: Factual, definition-based questions
    Complex: Comparative, analytical, multi-part questions
    """
    question = state["question"]

    prompt = ChatPromptTemplate.from_template(
        "Classifique a seguinte pergunta como 'simple' ou 'complex'.\n\n"
        "Simple: Perguntas factuais, definições, conceitos únicos.\n"
        "Complex: Perguntas comparativas, analíticas, múltiplas partes, explicações profundas.\n\n"
        "Pergunta: {question}\n\n"
        "Responda APENAS com 'simple' ou 'complex':"
    )

    chain = prompt | llm
    response = chain.invoke({"question": question})
    complexity = _normalize_complexity(str(response.content))

    print(f"[CLASSIFY] Question classified as: {complexity}")
    state["complexity"] = complexity
    return state


@traceable(run_type="retriever", name="Adaptive Document Retrieval")
def retrieve_adaptive(state: RAGState) -> RAGState:
    """
    Performs adaptive retrieval based on question complexity.

    With reranking enabled:
    - Simple questions: k=10 documents (then reranked to top 5)
    - Complex questions: k=15 documents (then reranked to top 7)

    Without reranking:
    - Simple questions: k=3 documents
    - Complex questions: k=7 documents
    """
    question = state["question"]
    complexity = state["complexity"]

    # Adaptive k selection
    # If reranking enabled, retrieve more docs for better reranking pool
    if settings.reranker_enabled:
        k = 10 if complexity == "simple" else 15
        print(
            f"[RETRIEVE] Retrieving {k} documents for {complexity} question (with reranking)"
        )
    else:
        k = 3 if complexity == "simple" else 7
        print(f"[RETRIEVE] Retrieving {k} documents for {complexity} question")

    # Load vectorstore and retrieve
    vectordb = FAISS.load_local(
        db_path, embeddings, allow_dangerous_deserialization=True
    )
    docs = vectordb.similarity_search(question, k=k)

    # Extract document content
    documents = [doc.page_content for doc in docs]

    print(f"[RETRIEVE] Retrieved {len(documents)} documents")
    state["documents"] = documents
    return state


@traceable(run_type="chain", name="BGE Semantic Reranking")
def rerank_documents(state: RAGState) -> RAGState:
    """
    Reranks retrieved documents using BGE cross-encoder for semantic relevance.

    This node is conditionally executed based on settings.reranker_enabled.
    If disabled, it passes through without modification (returns the current state).

    Process:
    1. Check if reranking is enabled
    2. Convert document strings to LangChain Document objects
    3. Apply BGE cross-encoder reranking
    4. Filter to top_n most relevant documents
    5. Convert back to strings

    Args:
        state: RAGState containing question and documents

    Returns:
        Dict with reranked documents, or empty dict if disabled
    """
    if not settings.reranker_enabled:
        print("[RERANK] Disabled - skipping reranking")
        return state

    question = state["question"]
    documents = state["documents"]
    complexity = state["complexity"]

    if not documents:
        print("[RERANK] No documents to rerank")
        return state

    print(f"[RERANK] Reranking {len(documents)} documents")

    # Determine top_n based on complexity (override settings)
    top_n = 5 if complexity == "simple" else 7

    reranked_content = apply_reranking(question, documents, top_n=top_n)

    print(f"[RERANK] Reranked {len(documents)} → {len(reranked_content)} documents")

    state["documents"] = reranked_content
    return state


@traceable(run_type="llm", name="Generate Answer")
def generate_answer(state: RAGState) -> RAGState:
    """
    Generates answer based on retrieved documents and question.
    Uses optimized prompt for RAG.
    """
    question = state["question"]
    documents = state["documents"]

    # Build context from documents
    contexto = "\n\n".join(
        [f"Documento {i+1}: {doc}" for i, doc in enumerate(documents)]
    )

    prompt = ChatPromptTemplate.from_template(
        "Você é um assistente especializado em responder perguntas com base em documentos fornecidos.\n\n"
        "INSTRUÇÕES:\n"
        "- Responda APENAS com base nos documentos abaixo\n"
        "- Se a informação não estiver nos documentos, diga claramente\n"
        "- Seja preciso e completo\n"
        "- Use exemplos dos documentos quando relevante\n\n"
        "DOCUMENTOS:\n{contexto}\n\n"
        "PERGUNTA: {pergunta}\n\n"
        "RESPOSTA:"
    )

    chain = prompt | llm
    response = chain.invoke({"contexto": contexto, "pergunta": question})
    generation = str(response.content)

    print(f"[GENERATE] Generated answer ({len(generation)} chars)")
    state["generation"] = generation
    return state


@traceable(run_type="chain", name="Validate Answer Quality")
def validate_quality(state: RAGState) -> RAGState:
    """
    Validates answer quality using LLM-as-judge.
    Returns quality score between 0 and 1.
    Criteria: Relevance, completeness, accuracy
    """
    question = state["question"]
    generation = state["generation"]
    documents = state["documents"]

    contexto = "\n".join(documents[:3])  # Use first 3 docs for validation

    prompt = ChatPromptTemplate.from_template(
        "Avalie a qualidade da resposta abaixo em uma escala de 0 a 1.\n\n"
        "CRITÉRIOS:\n"
        "- Relevância: A resposta responde a pergunta?\n"
        "- Completude: A resposta é suficientemente completa?\n"
        "- Precisão: A resposta está baseada nos documentos?\n\n"
        "PERGUNTA: {question}\n\n"
        "DOCUMENTOS DISPONÍVEIS:\n{contexto}\n\n"
        "RESPOSTA:\n{generation}\n\n"
        "Responda APENAS com um número entre 0 e 1 (ex: 0.85):"
    )

    chain = prompt | llm
    response = chain.invoke(
        {"question": question, "contexto": contexto, "generation": generation}
    )

    try:
        quality_score = float(str(response.content).strip())
        # Clamp between 0 and 1
        quality_score = max(0.0, min(1.0, quality_score))
    except ValueError:
        # Default to medium quality if parsing fails
        quality_score = 0.6

    print(f"[VALIDATE] Quality score: {quality_score:.2f}")
    state["quality_score"] = quality_score
    return state


@traceable(run_type="chain", name="Refine Answer with Feedback")
def refine_answer(state: RAGState) -> RAGState:
    """
    Refines answer based on validation feedback.
    Attempts to improve quality by re-generating with explicit feedback.
    """
    question = state["question"]
    documents = state["documents"]
    previous_generation = state["generation"]
    quality_score = state["quality_score"]
    iterations = state.get("iterations", 0)

    contexto = "\n\n".join(
        [f"Documento {i+1}: {doc}" for i, doc in enumerate(documents)]
    )

    prompt = ChatPromptTemplate.from_template(
        "Você precisa MELHORAR a resposta anterior que recebeu score de qualidade {score:.2f}.\n\n"
        "RESPOSTA ANTERIOR:\n{previous}\n\n"
        "INSTRUÇÕES PARA MELHORIA:\n"
        "- Use mais detalhes dos documentos\n"
        "- Seja mais preciso e completo\n"
        "- Adicione exemplos relevantes\n"
        "- Mantenha foco na pergunta\n\n"
        "DOCUMENTOS:\n{contexto}\n\n"
        "PERGUNTA: {pergunta}\n\n"
        "RESPOSTA MELHORADA:"
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "score": quality_score,
            "previous": previous_generation,
            "contexto": contexto,
            "pergunta": question,
        }
    )

    refined_generation = str(response.content)
    new_iterations = iterations + 1

    print(f"[REFINE] Refined answer (iteration {new_iterations})")
    state["generation"] = refined_generation
    state["iterations"] = new_iterations
    return state
