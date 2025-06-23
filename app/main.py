import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.query_llm import get_llm_answer

app = FastAPI(title="UC AI Chatbot (Optimized)")

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    text = question.strip().lower()
    if text in {"hi", "hello", "hey", "hi there"}:
        answer = "👋 Hello Bearcat! How can I help you today?"
    else:
        answer = await get_llm_answer(question)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "question": question, "response": answer},
    )
