import os
import warnings

from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src.infrastructure.config.settings import settings

# Verify Configuration
print("=" * 80)
print("SYSTEM CONFIGURATION (Pydantic Settings)")
print("=" * 80)
print(f"LANGSMITH_TRACING: {settings.langsmith_tracing}")
print(f"LANGSMITH_PROJECT: {settings.langsmith_project}")
print(f"LANGSMITH_API_KEY: {'***' if settings.langsmith_api_key else 'NOT SET'}")
print(f"GOOGLE_API_KEY: {'***' if settings.google_api_key else 'NOT SET'}")
print(f"LLM_MODEL: {settings.llm_model}")
print("=" * 80 + "\n")

caminho_pdf = "Perceptron.pdf"
loader = PyPDFLoader(caminho_pdf)
documentos = loader.load()


def train_model():
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunk = splitter.split_documents(documentos)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db_path = "banco_faiss"
    if os.path.exists(db_path):
        vectordb = FAISS.load_local(
            db_path, embeddings, allow_dangerous_deserialization=True
        )
        vectordb.add_documents(chunk)
    else:
        vetorstore = FAISS.from_documents(chunk, embeddings)
        vetorstore.save_local(db_path)


def retrieval(pergunta: str = "Quais as limitações do Perceptron?"):
    """
    Legacy retrieval function - kept for backwards compatibility.
    For new usage, prefer using graph_rag.run_rag_query()
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db_path = "banco_faiss"
    vectordb = FAISS.load_local(
        db_path, embeddings, allow_dangerous_deserialization=True
    )
    docs = vectordb.similarity_search(pergunta, k=5)

    contexto = "\n\n".join([f"Material: {doc.page_content}" for doc in docs])

    prompt = ChatPromptTemplate.from_template(
        "Você é um assistente especializado.\n"
        "Responda a pergunta do usuário SOMENTE com base no contexto abaixo.\n"
        "Se não houver informação suficiente, diga isso claramente.\n\n"
        "Contexto:\n{contexto}\n\n"
        "Pergunta: {pergunta}\n\n"
    )

    llm = ChatGoogleGenerativeAI(model=settings.llm_model, temperature=0)

    chain = prompt | llm
    resposta = chain.invoke({"contexto": contexto, "pergunta": pergunta})
    return resposta.content


from src.core.services.memory_manager import get_conversation_config, reset_conversation

# Import conversational RAG system
from src.features.conversation.conversation_graph import run_conversational_query

# Import new LangGraph RAG system
from src.features.rag.graph_rag import run_rag_query

# Test both systems
print("=" * 80)
print("TESTING LANGGRAPH RAG SYSTEM (Single-turn)")
print("=" * 80)

pergunta_teste = "Quais as limitações do Perceptron?"
resposta_graph = run_rag_query(pergunta_teste)

print("\n" + "=" * 80)
print("FINAL ANSWER:")
print("=" * 80)
print(resposta_graph)

# Test conversational system
print("\n\n" + "=" * 80)
print("TESTING CONVERSATIONAL RAG SYSTEM (Multi-turn)")
print("=" * 80)

# Reset conversation for fresh start
reset_conversation("test_user")
config = get_conversation_config("test_user")

# Turn 1: Initial question
print("\n[Turn 1] User: O que é Perceptron?")
response1 = run_conversational_query("O que é Perceptron?", "test_user", config)
print(f"\nAssistant: {response1}\n")

# Turn 2: Follow-up question with pronoun
print("\n[Turn 2] User: Quais suas limitações?")
response2 = run_conversational_query("Quais suas limitações?", "test_user", config)
print(f"\nAssistant: {response2}\n")

# Turn 3: Another follow-up
print("\n[Turn 3] User: E como resolver isso?")
response3 = run_conversational_query("E como resolver isso?", "test_user", config)
print(f"\nAssistant: {response3}\n")

print("\n" + "=" * 80)
print("CONVERSATIONAL TEST COMPLETE!")
print("=" * 80)
print("\nTo start interactive chat mode, run:")
print("  python chat.py")
print("=" * 80 + "\n")
