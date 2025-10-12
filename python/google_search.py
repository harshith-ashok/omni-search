import requests
from bs4 import BeautifulSoup


class DuckDuckGoSearch:
    def __init__(self):
        self.base_url = "https://html.duckduckgo.com/html/"

    def search(self, query, num_results=5):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        data = {"q": query}

        response = requests.post(
            self.base_url, headers=headers, data=data, timeout=5)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for link in soup.select("a.result__a")[:num_results]:
            title = link.get_text(strip=True)
            url = link["href"]
            snippet_tag = link.find_parent(
                "div", class_="result").select_one("a.result__snippet")
            snippet = snippet_tag.get_text(
                " ", strip=True) if snippet_tag else ""

            results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })

        return results
