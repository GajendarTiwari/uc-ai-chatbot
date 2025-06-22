# models/query_llm.py
import os
from dotenv import load_dotenv

from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1️⃣ Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ Missing GOOGLE_API_KEY in `.env`")

# 2️⃣ Embedding Function
hf_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3️⃣ Chroma VectorDB path
CHROMA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "embeddings", "chroma_db"))
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=hf_embedding)

# 4️⃣ Sanity Check
try:
    count = vectordb._collection.count()
except Exception as e:
    raise RuntimeError(f"❌ Unable to access ChromaDB at {CHROMA_DIR}: {e}")
print(f"[DEBUG] ✅ ChromaDB contains {count} chunks.")
if count == 0:
    raise RuntimeError("❌ No embeddings found. Run `embedder.py` first!")

# 5️⃣ Retriever Configuration
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# 6️⃣ Prompt Template (unchanged)
template = """
You are a UC admissions expert.
Given the excerpts below, summarize in 3–4 sentences the specific graduate admission requirements at the University of Cincinnati.
If a requirement isn’t in the excerpts, say “Not specified.”

Excerpts:
{context}

Question:
{question}

Answer:
"""
prompt = PromptTemplate(input_variables=["context", "question"], template=template)

# 7️⃣ Gemini 2.0 Flash LLM (unchanged model name)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    google_api_key=GOOGLE_API_KEY,
)

# 8️⃣ Retrieval QA Chain (unchanged logic)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# ✅ Exposed function for backend
def get_llm_response(question: str):
    """
    Returns a tuple (answer: str, sources: List[str]).
    """
    print(f"[QUERY] 📥 Received question: {question}")
    try:
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        # extract basename of each source for clarity
        sources = [
            os.path.basename(doc.metadata.get("source", "Unknown"))
            for doc in result.get("source_documents", [])
        ]
        # dedupe preserving order
        seen = set()
        deduped = []
        for s in sources:
            if s not in seen:
                seen.add(s)
                deduped.append(s)
        print(f"[RESULT] 📤 Answer: {answer}\n        Sources: {deduped}")
        return answer, deduped
    except Exception as e:
        print(f"[ERROR] ❌ An error occurred in get_llm_response: {e}")
        # Return a friendly error message to user
        return "⚠️ Sorry, I couldn’t process that. Please try again.", []
