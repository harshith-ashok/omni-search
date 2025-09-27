from fastapi import FastAPI, Query
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI(title="Custom Web Scraper API built for OmniSearch")


def scrape_page(url: str) -> Dict:
    """
    Fetches a web page, extracts visible text and links.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract text (remove script/style)
    for script in soup(["script", "style"]):
        script.extract()

    text = " ".join(soup.stripped_strings)

    # Extract links
    links = []
    for a in soup.find_all("a", href=True):
        full_url = urljoin(url, a["href"])
        links.append(full_url)

    return {"url": url, "text_snippet": text[:500], "links": links[:10]}


@app.get("/scrape")
def scrape(urls: List[str] = Query(..., description="List of URLs to scrape")):
    """
    Scrape one or more URLs and return their text + links.
    """
    results = []
    for url in urls:
        try:
            data = scrape_page(url)
            results.append(data)
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    return {"results": results}
