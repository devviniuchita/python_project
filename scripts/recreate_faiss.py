"""
Script para recriar o banco FAISS com Google Embeddings
"""

import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Load environment variables
venv_env_path = "c:/Users/ADMIN/Desktop/rules-base/.venv/.env"
if os.path.exists(venv_env_path):
    load_dotenv(venv_env_path)
    print(f"[ENV] Loaded from: {venv_env_path}")

print("[INFO] Recreating FAISS database with Google embeddings...")

# Load PDF
caminho_pdf = "Perceptron.pdf"
loader = PyPDFLoader(caminho_pdf)
documentos = loader.load()
print(f"[INFO] Loaded {len(documentos)} pages from PDF")

# Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documentos)
print(f"[INFO] Created {len(chunks)} chunks")

# Create embeddings with Google
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
print("[INFO] Using Google embeddings model: models/embedding-001")

# Create and save FAISS vectorstore
db_path = 'banco_faiss'
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(db_path)

print(f"[SUCCESS] FAISS database created at: {db_path}")
print(f"[SUCCESS] Total vectors: {len(chunks)}")
print("[SUCCESS] Ready to use with Google Gemini API!")
