from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.assistant import run_user_message
from core.llm import clear_chat_history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.36:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    
@app.get("/")
def home():
    return {"status": "Assitant backend running!"}
    
@app.post("/text")
def text_mode(req: ChatRequest):
    result = run_user_message(req.message)
    return result

@app.post("/new-chat")
def new_chat():
    clear_chat_history()
    return {"status" : "New Chat Started!"}