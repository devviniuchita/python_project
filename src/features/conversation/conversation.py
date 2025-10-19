"""
Conversational Nodes for RAG System
Handles context analysis, follow-up detection, and question expansion
"""

from typing import Any

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable

from src.core.domain.state import ConversationalRAGState
from src.infrastructure.config.settings import settings

# Initialize LLM
llm = ChatGoogleGenerativeAI(model=settings.llm_model, temperature=0)


def _coerce_content(content: Any) -> str:
    """Normalize message or LLM content to a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(str(part) for part in content)
    return str(content)


@traceable(run_type="chain", name="Analyze Context for Follow-up")
def analyze_context(state: ConversationalRAGState) -> ConversationalRAGState:
    """
    Analyzes if the current question is a follow-up or standalone.

    Detects:
    - Pronouns (isso, aquilo, ele, ela, etc.)
    - Demonstratives (este, esse, aquele)
    - Implicit references
    - Continuation patterns

    Returns:
        Dict with is_followup, question, original_question fields
    """
    messages = state["messages"]
    current_question = _coerce_content(messages[-1].content) if messages else ""

    # Store original question
    original_question = current_question

    # If first message, can't be follow-up
    if len(messages) <= 1:
        print("[CONTEXT] First message - not a follow-up")
        state["is_followup"] = False
        state["question"] = current_question
        state["original_question"] = original_question
        return state

    # Get recent conversation history (last 4 messages)
    recent_messages = messages[-4:] if len(messages) > 4 else messages[:-1]
    history_text = "\n".join(
        [
            f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {_coerce_content(msg.content)}"
            for msg in recent_messages
        ]
    )

    # Use LLM to detect follow-up
    prompt = ChatPromptTemplate.from_template(
        "Analise se a pergunta atual é uma pergunta de follow-up (continuação) "
        "ou uma pergunta nova e independente.\n\n"
        "HISTÓRICO RECENTE:\n{history}\n\n"
        "PERGUNTA ATUAL: {question}\n\n"
        "Uma pergunta de follow-up:\n"
        "- Usa pronomes (isso, aquilo, ele, ela, disso)\n"
        "- Usa demonstrativos (este, esse, aquele)\n"
        "- Referencia implicitamente o tópico anterior\n"
        "- Pede mais detalhes sobre resposta anterior\n"
        '- Usa "E...?", "Mas...", "Também..."\n\n'
        "Responda APENAS 'sim' (é follow-up) ou 'não' (pergunta nova):"
    )

    chain = prompt | llm
    response = chain.invoke({"history": history_text, "question": current_question})

    # Safely extract content (can be str or list in some cases)
    is_followup_text = _coerce_content(response.content).lower()

    is_followup = "sim" in is_followup_text

    if is_followup:
        print(f"[CONTEXT] Detected follow-up question: {current_question}")
    else:
        print(f"[CONTEXT] Standalone question: {current_question}")

    state["is_followup"] = is_followup
    state["question"] = current_question  # Will be expanded later if follow-up
    state["original_question"] = original_question
    return state


@traceable(run_type="chain", name="Expand Follow-up Question")
def expand_question(state: ConversationalRAGState) -> ConversationalRAGState:
    """
    Expands follow-up questions with context from conversation history.

    Converts implicit references to explicit questions for better retrieval.
    Example:
        History: "O que é Perceptron?" -> "É uma rede neural..."
        Follow-up: "Quais suas limitações?"
        Expanded: "Quais as limitações do Perceptron?"

    Returns:
        Dict with expanded question field
    """
    if not state["is_followup"]:
        # Not a follow-up, return as-is
        print("[EXPAND] Standalone question - no expansion needed")
        return state

    messages = state["messages"]
    current_question = state["original_question"]

    # Get recent conversation (last 6 messages for context)
    recent_messages = messages[-6:] if len(messages) > 6 else messages[:-1]
    history_text = "\n".join(
        [
            f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {_coerce_content(msg.content)}"
            for msg in recent_messages
        ]
    )

    # Use LLM to expand question with context
    prompt = ChatPromptTemplate.from_template(
        "Reescreva a pergunta de follow-up como uma pergunta completa e autônoma, "
        "incorporando o contexto necessário do histórico da conversa.\n\n"
        "HISTÓRICO DA CONVERSA:\n{history}\n\n"
        "PERGUNTA DE FOLLOW-UP: {question}\n\n"
        "INSTRUÇÕES:\n"
        "- Substitua pronomes por entidades específicas\n"
        "- Torne a pergunta compreensível sem o histórico\n"
        "- Mantenha a intenção original da pergunta\n"
        "- Seja conciso mas completo\n\n"
        "PERGUNTA EXPANDIDA:"
    )

    chain = prompt | llm
    response = chain.invoke({"history": history_text, "question": current_question})

    # Safely extract content
    expanded_question = _coerce_content(response.content).strip()

    print(f"[EXPAND] Original: {current_question}")
    print(f"[EXPAND] Expanded: {expanded_question}")

    state["question"] = expanded_question
    return state


@traceable(run_type="chain", name="Check if Clarification Needed")
def check_clarification(state: ConversationalRAGState) -> ConversationalRAGState:
    """
    Checks if the question is ambiguous and needs clarification.

    Returns clarification question if needed, otherwise proceeds normally.

    Returns:
        Dict with generation and quality_score if clarification needed, empty dict otherwise
    """
    question = state["question"]
    documents = state["documents"]

    # If no documents retrieved, might need clarification
    if not documents:
        prompt = ChatPromptTemplate.from_template(
            "Analise se a seguinte pergunta é clara o suficiente ou se precisa de clarificação.\n\n"
            "PERGUNTA: {question}\n\n"
            "Uma pergunta precisa de clarificação se:\n"
            "- É muito vaga ou genérica\n"
            "- Tem múltiplas interpretações possíveis\n"
            "- Falta contexto essencial\n\n"
            "Responda APENAS 'sim' (precisa clarificação) ou 'não' (está clara):"
        )

        chain = prompt | llm
        response = chain.invoke({"question": question})

        # Safely extract content
        response_text = _coerce_content(response.content).lower()

        needs_clarification = "sim" in response_text

        if needs_clarification:
            # Generate clarification question
            clarification_prompt = ChatPromptTemplate.from_template(
                "Gere uma pergunta de clarificação educada e específica para ajudar "
                "o usuário a reformular a pergunta de forma mais clara.\n\n"
                "PERGUNTA VAGA: {question}\n\n"
                "PERGUNTA DE CLARIFICAÇÃO:"
            )

            clarification_chain = clarification_prompt | llm
            clarification_response = clarification_chain.invoke({"question": question})

            # Safely extract clarification content
            clarification = _coerce_content(clarification_response.content).strip()

            print(f"[CLARIFY] Needs clarification: {question}")
            print(f"[CLARIFY] Asking: {clarification}")

            state["generation"] = (
                f"Desculpe, preciso de mais informações. {clarification}"
            )
            state["quality_score"] = 0.5  # Medium score - needs user input
            return state

    print("[CLARIFY] Question is clear enough")
    return state
