from fastapi import FastAPI, Query
from typing import List
from crawler import scrape_page
from indexer import SimpleIndexer

app = FastAPI(title="Mini Search Engine")
indexer = SimpleIndexer()


@app.post("/crawl")
def crawl_and_index(urls: List[str]):
    """
    Crawl the given URLs and add them to the index.
    """
    docs = []
    for url in urls:
        try:
            page = scrape_page(url)
            indexer.add_document(page["url"], page["text"])
            docs.append({"url": url, "status": "indexed"})
        except Exception as e:
            docs.append({"url": url, "error": str(e)})
    return {"indexed": docs}


@app.get("/search")
def search(query: str = Query(..., description="Search term")):
    """
    Search for a term in the indexed pages.
    """
    results = indexer.search(query)
    return {"query": query, "results": results}
