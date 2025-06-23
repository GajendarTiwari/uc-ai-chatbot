from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

from models.query_llm import get_llm_answer  # Make sure this import path is correct

app = FastAPI()

# Define base directory (app/)
BASE_DIR = Path(__file__).resolve().parent

# Mount static directory (app/static)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Set templates directory (app/templates)
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": ""})

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, user_input: str = Form(...)):
    try:
        # Call your LLM or vector search logic here
        response = await get_llm_answer(user_input)
    except Exception as e:
        response = f"❌ Error processing request: {str(e)}"
    return templates.TemplateResponse("index.html", {"request": request, "response": response})
