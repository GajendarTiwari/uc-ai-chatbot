 🧠 UC AI Chatbot

An intelligent chatbot system built to assist users with University of Cincinnati-related queries, powered by Retrieval-Augmented Generation (RAG) using Google Gemini Pro (Flash 1.5), LangChain, and Chroma vector database.

---

## 📌 Project Overview

The **UC AI Chatbot** is a full-stack AI application designed to provide intelligent, real-time answers about graduate admissions, academics, and university services at the University of Cincinnati. It uses state-of-the-art retrieval-based natural language processing with vector search and LLM-based reasoning.

---

## 🚀 Key Features

- 🔍 **Semantic Search with Vector Embeddings**  
  Documents scraped from UC websites are converted to dense vector embeddings for semantic retrieval.

- 🤖 **LLM-Powered Reasoning**  
  Integrated with Google Gemini Flash 1.5 using LangChain’s `ChatGoogleGenerativeAI` for accurate, contextual responses.

- 🧱 **Modular Backend Architecture**  
  Built using **FastAPI** for high performance, with modular folders for crawling, embeddings, and model logic.

- 💬 **Interactive Chat Interface**  
  Clean and responsive frontend with HTML + CSS that simulates a chat experience (submission and bot feedback).

- 🌐 **Portable & Cloud-Ready Deployment**  
  Easily deployable on Render, Railway, or Vercel with minimal configuration.

---

## 🏗️ Architecture

uc-ai-chatbot/
│
├── app/
│ ├── main.py # FastAPI app with web routes
│ ├── templates/index.html # Frontend chat UI
│ ├── static/style.css # Chatbot styling
│
├── crawler/
│ ├── crawler.py # UC website scraper
│ └── data/pages/ # Scraped HTML content
│
├── embeddings/
│ └── embedder.py # Chroma vector DB creation
│
├── models/
│ └── query_llm.py # LLM QA chain setup
│
├── .env # API keys and config
├── requirements.txt # Python dependencies
├── render.yaml # Render deployment configuration (optional)
└── README.md # You’re here!
## ⚙️ Technologies Used

| Category       | Tools/Frameworks                          |
|----------------|-------------------------------------------|
| 🧠 LLM          | Google Gemini 1.5 Flash (via LangChain)   |
| 📦 Embeddings  | HuggingFace `all-MiniLM-L6-v2`            |
| 🔍 Vector DB    | Chroma                                    |
| 🚀 Web Framework | FastAPI                                   |
| 🎨 Frontend     | HTML, CSS (static/chat UI)                |
| 🧪 Others       | `python-multipart`, `uvicorn`, `dotenv`  |

---
2. Install Dependencies
pip install -r requirements.txt
3. Set Up .env
Create a .env file in the root directory:
env
GOOGLE_API_KEY=your_google_api_key
CHROMA_DB_DIR=embeddings/chroma_db
4. Run the Application
uvicorn app.main:app --reload
Access the chatbot at: http://localhost:8000

💻 Deployment (Optional)
If you're deploying on Render, include render.yaml.
If using Vercel or Railway, configure build and start scripts in your dashboard or via vercel.json.
Status & Limitations
✅ Backend + LLM pipeline complete
✅ Frontend chat UI working
⚠️ Deployment may exceed free-tier limits on Render or Railway due to LLM + embedding model size
📚 Skills Demonstrated
🔧 Backend API Development (FastAPI)
🤖 LLM Integration (Google Gemini Flash 1.5 via LangChain)
📊 Semantic Search & Vector DB (Chroma)
🧠 Prompt Engineering & RetrievalQA Chains
💻 Full-stack system design with modular folder structure
🛠️ Deployment Readiness (Render, Vercel, Railway)
