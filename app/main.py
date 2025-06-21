import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.query_llm import get_llm_response

app = FastAPI()

# Mount static files
BASE_DIR = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Template setup
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    text = question.strip().lower()
    if text in {"hi", "hello", "hey"}:
        response = "Hello Bearcat!"
    else:
        response, _ = get_llm_response(question)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question,
        "response": response
    })
