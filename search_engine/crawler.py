import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_page(url: str):
    """
    Scrape a single web page: extract text + links.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # remove unwanted elements
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = " ".join(soup.stripped_strings)

    links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]

    return {"url": url, "text": text, "links": links}
