from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

from models.query_llm import get_llm_answer

app = FastAPI()

# Base directory (app/)
BASE_DIR = Path(__file__).resolve().parent

# Mount static folder
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Load templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    try:
        answer = await get_llm_answer(question)
    except Exception as e:
        print("❌ Error from get_llm_answer:", e)
        answer = "⚠️ Sorry, something went wrong."
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question,
        "response": answer
    })
