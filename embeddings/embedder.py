# embeddings/embedder.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load .env for any config (not strictly needed here)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, "../crawler/data/pages"))
CHROMA_DIR = os.path.normpath(os.path.join(BASE_DIR, "chroma_db"))

def embed_docs() -> None:
    print("[INFO] Loading documents from:", DATA_DIR)
    docs = []
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".txt"):
            continue
        full_path = os.path.join(DATA_DIR, fname)
        loader = TextLoader(full_path, encoding="utf-8")
        docs.extend(loader.load())

    print(f"[INFO] {len(docs)} docs loaded. Splitting…")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print(f"[INFO] Embedding {len(chunks)} chunks…")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    # In recent versions, .persist() is automatic
    print(f"[INFO] Saved Chroma DB to {CHROMA_DIR}")

if __name__ == "__main__":
    embed_docs()
