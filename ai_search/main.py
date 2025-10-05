from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import BaymaxChat

app = FastAPI(title="Baymax Chatbot")
baymax = BaymaxChat()

# CORS middleware to handle preflight OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Adjust in production to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],      # Allows POST, OPTIONS, GET, etc.
    allow_headers=["*"],
)

# Request model


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"  # Optional: allows multiple users

# Chat endpoint


@app.post("/chat")
def chat(request: ChatRequest):
    reply = baymax.chat(request.message, session_id=request.session_id)
    return {"reply": reply}