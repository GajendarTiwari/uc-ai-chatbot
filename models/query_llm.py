import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in environment")

TEMPLATE = """
You are a UC admissions expert.
Given the excerpts below, summarize in 3–4 sentences the specific graduate admission requirements at the University of Cincinnati.
If a requirement isn’t in the excerpts, say “Not specified.”

Excerpts:
{context}

Question:
{question}

Answer:
"""

async def get_llm_answer(question: str) -> str:
    try:
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = Chroma(
            persist_directory=os.getenv("CHROMA_DB_DIR", "embeddings/chroma_db"),
            embedding_function=embedder,
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        prompt = PromptTemplate(input_variables=["context", "question"], template=TEMPLATE)
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.2, 
            google_api_key=GOOGLE_API_KEY
        )

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=False,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt}
        )
        result = await chain.acall({"query": question})
        return result["result"]

    except Exception as e:
        print("❌ LLM failure:", e)
        return "⚠️ Sorry, an error occurred while processing your question."
