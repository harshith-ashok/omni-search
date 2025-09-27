import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class WebCrawler:
    def __init__(self, max_pages=10):
        self.max_pages = max_pages
        self.visited = set()

    def crawl(self, start_url, keyword=None):
        results = []
        queue = deque([start_url])

        while queue and len(self.visited) < self.max_pages:
            url = queue.popleft()
            if url in self.visited:
                continue

            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                self.visited.add(url)

                title = soup.title.string.strip() if soup.title else "No Title"
                text = soup.get_text(" ", strip=True)
                snippet = " ".join(text.split()[:50])  # First 50 words

                if not keyword or keyword.lower() in text.lower() or keyword.lower() in title.lower():
                    results.append({
                        "url": url,
                        "title": title,
                        "snippet": snippet
                    })

                # Collect links
                for link_tag in soup.find_all("a", href=True):
                    href = link_tag["href"]
                    full_url = urljoin(url, href)
                    if self._is_valid_url(full_url):
                        queue.append(full_url)

            except Exception:
                continue

        return results

    def _is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
