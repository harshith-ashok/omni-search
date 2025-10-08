from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import BaymaxChat
import os

LIST = ['Desktop', 'Downloads', 'Documents', 'Pictures', 'Movies', 'Music']
HOME = '/Users/harshith/'

app = FastAPI(title="Baymax Chatbot")
baymax = BaymaxChat()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


'''
curl http://127.0.0.1:8000/local\?query\=".js"
'''


@app.get("/local")
def search(
    query: str = Query(..., description="File name to search for"),
):
    results = []
    for folder in LIST:
        folder_path = os.path.join(HOME, folder)
        if not os.path.isdir(folder_path):
            continue
        for f in os.listdir(folder_path):
            if not f.startswith('.') and query.lower() in f.lower():
                results.append({"folder": folder, "file": f})
    return {"results": results}


'''
curl http://127.0.0.1:8000/local-deep\?query\=".js"
'''


@app.get("/local-deep")
def search_deep(
    query: str = Query(..., description="File name to search for"),
):
    results = []
    for folder in LIST:
        folder_path = os.path.join(HOME, folder)
        if not os.path.isdir(folder_path):
            continue
        for root, dirs, files in os.walk(folder_path):
            rel_path = os.path.relpath(root, folder_path)
            depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
            if depth > 4:
                dirs[:] = []
                continue
            for f in files:
                if not f.startswith('.') and query.lower() in f.lower():
                    results.append({
                        "folder": folder,
                        "subfolder": os.path.relpath(root, folder_path) if root != folder_path else "",
                        "file": f
                    })
    return {"results": results}


'''
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"session_id": "user123", "message": "Mount Everest"}'
'''


@app.post("/chat")
def chat(request: ChatRequest):
    reply = baymax.chat(request.message, session_id=request.session_id)
    return {"reply": reply}
