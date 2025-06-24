from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from app.models.query_llm import get_llm_answer

app = FastAPI()

# Mount static folder properly (use absolute path for Render)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    response = await get_llm_answer(question)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "question": question,
        "response": response
    })

# Needed to run locally and for explicit Render startup command
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000)
