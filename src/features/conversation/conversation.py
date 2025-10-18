"""
Conversational Nodes for RAG System
Handles context analysis, follow-up detection, and question expansion
"""

import os

from typing import Any
from typing import Dict

from src.infrastructure.config.settings import settings
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from src.core.domain.state import ConversationalRAGState


# Initialize LLM
llm = ChatGoogleGenerativeAI(model=settings.llm_model, temperature=0)


@traceable(run_type="chain", name="Analyze Context for Follow-up")
def analyze_context(state: ConversationalRAGState) -> Dict[str, Any]:
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
    current_question = messages[-1].content if messages else ""

    # Store original question
    original_question = current_question

    # If first message, can't be follow-up
    if len(messages) <= 1:
        print("[CONTEXT] First message - not a follow-up")
        return {
            "is_followup": False,
            "question": current_question,
            "original_question": original_question,
        }

    # Get recent conversation history (last 4 messages)
    recent_messages = messages[-4:] if len(messages) > 4 else messages[:-1]
    history_text = "\n".join(
        [
            f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
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
        "- Usa \"E...?\", \"Mas...\", \"Também...\"\n\n"
        "Responda APENAS 'sim' (é follow-up) ou 'não' (pergunta nova):"
    )

    chain = prompt | llm
    response = chain.invoke({"history": history_text, "question": current_question})

    # Safely extract content (can be str or list in some cases)
    content = response.content
    if isinstance(content, str):
        is_followup_text = content.strip().lower()
    elif isinstance(content, list):
        # Join list parts if multimodal response
        is_followup_text = " ".join(str(part) for part in content).lower()
    else:
        is_followup_text = str(content).lower()

    is_followup = "sim" in is_followup_text

    if is_followup:
        print(f"[CONTEXT] Detected follow-up question: {current_question}")
    else:
        print(f"[CONTEXT] Standalone question: {current_question}")

    return {
        "is_followup": is_followup,
        "question": current_question,  # Will be expanded later if follow-up
        "original_question": original_question,
    }


@traceable(run_type="chain", name="Expand Follow-up Question")
def expand_question(state: ConversationalRAGState) -> Dict[str, Any]:
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
    if not state.get("is_followup", False):
        # Not a follow-up, return as-is
        print("[EXPAND] Standalone question - no expansion needed")
        return {}

    messages = state["messages"]
    current_question = state["original_question"]

    # Get recent conversation (last 6 messages for context)
    recent_messages = messages[-6:] if len(messages) > 6 else messages[:-1]
    history_text = "\n".join(
        [
            f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
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
    content = response.content
    if isinstance(content, str):
        expanded_question = content.strip()
    elif isinstance(content, list):
        expanded_question = " ".join(str(part) for part in content)
    else:
        expanded_question = str(content)

    print(f"[EXPAND] Original: {current_question}")
    print(f"[EXPAND] Expanded: {expanded_question}")

    return {"question": expanded_question}


@traceable(run_type="chain", name="Check if Clarification Needed")
def check_clarification(state: ConversationalRAGState) -> Dict[str, Any]:
    """
    Checks if the question is ambiguous and needs clarification.

    Returns clarification question if needed, otherwise proceeds normally.

    Returns:
        Dict with generation and quality_score if clarification needed, empty dict otherwise
    """
    question = state["question"]
    documents = state.get("documents", [])

    # If no documents retrieved, might need clarification
    if not documents or len(documents) == 0:
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
        content = response.content
        if isinstance(content, str):
            response_text = content.strip().lower()
        elif isinstance(content, list):
            response_text = " ".join(str(part) for part in content).lower()
        else:
            response_text = str(content).lower()

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
            clarif_content = clarification_response.content
            if isinstance(clarif_content, str):
                clarification = clarif_content.strip()
            elif isinstance(clarif_content, list):
                clarification = " ".join(str(part) for part in clarif_content)
            else:
                clarification = str(clarif_content)

            print(f"[CLARIFY] Needs clarification: {question}")
            print(f"[CLARIFY] Asking: {clarification}")

            return {
                "generation": f"Desculpe, preciso de mais informações. {clarification}",
                "quality_score": 0.5,  # Medium score - needs user input
            }

    print("[CLARIFY] Question is clear enough")
    return {}  # Proceed normally
