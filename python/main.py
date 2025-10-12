from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google_search import DuckDuckGoSearch
from indexer import Indexer
from llm import BaymaxChat
import os

LIST = ['Desktop', 'Downloads', 'Documents', 'Pictures', 'Movies', 'Music']
HOME = '/Users/harshith/'

app = FastAPI(title="Baymax Chatbot")
baymax = BaymaxChat()

gsearch = DuckDuckGoSearch()
indexer = Indexer(index_file="index.json")


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


'''
curl -X POST "http://127.0.0.1:8000/index?start_url=https://harshithashok.com&max_pages=3"
'''


@app.post("/index")
def index_site(
    start_url: str = Query(..., description="URL to start indexing"),
    max_pages: int = Query(5, description="Max pages to crawl")
):
    data = indexer.build_index(start_url=start_url, max_pages=max_pages)
    return {"indexed": len(data), "data": data}


'''
curl "http://127.0.0.1:8000/search?query='hello'"
'''


@app.get("/search")
def search_index(query: str = Query(..., description="Search term")):
    results = indexer.search_index(query)
    return {"query": query, "results": results}


'''
curl "http://127.0.0.1:8000/gquery?query='hello'&num_results=5"
'''


@app.get("/gquery")
def google_query(
    query: str = Query(..., description="Search term"),
    num_results: int = Query(5, description="Number of results to fetch")
):
    results = gsearch.search(query, num_results=num_results)
    return {"query": query, "results": results}
