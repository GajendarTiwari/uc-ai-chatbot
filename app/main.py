from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.query_llm import get_llm_answer

app = FastAPI()

# Mount static folder if you have images or CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    return FileResponse("templates/index.html")


@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, user_question: str = Form(...)):
    try:
        # Get the answer from your Gemini / LLM logic
        bot_answer = get_llm_answer(user_question)
    except Exception as e:
        bot_answer = f"An error occurred: {str(e)}"

    # Render the HTML template again with the answer
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_question": user_question,
        "bot_answer": bot_answer
    })
