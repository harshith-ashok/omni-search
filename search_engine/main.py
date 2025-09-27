from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from indexer import Indexer
from google_search import DuckDuckGoSearch

app = FastAPI(title="Indexed Mini Search Engine")
gsearch = DuckDuckGoSearch()
indexer = Indexer(index_file="index.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/index")
def index_site(
    start_url: str = Query(..., description="URL to start indexing"),
    max_pages: int = Query(5, description="Max pages to crawl")
):
    data = indexer.build_index(start_url=start_url, max_pages=max_pages)
    return {"indexed": len(data), "data": data}


@app.get("/search")
def search_index(query: str = Query(..., description="Search term")):
    results = indexer.search_index(query)
    return {"query": query, "results": results}


@app.get("/gquery")
def google_query(
    query: str = Query(..., description="Search term"),
    num_results: int = Query(5, description="Number of results to fetch")
):
    results = gsearch.search(query, num_results=num_results)
    return {"query": query, "results": results}
