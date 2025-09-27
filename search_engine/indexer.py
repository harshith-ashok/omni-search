from typing import List, Dict
import re


class SimpleIndexer:
    def __init__(self):
        self.index = {}   # word → list of (url, snippet)

    def add_document(self, url: str, text: str):
        words = re.findall(r"\w+", text.lower())
        snippet = text[:300]
        for word in set(words):
            if word not in self.index:
                self.index[word] = []
            self.index[word].append((url, snippet))

    def search(self, query: str) -> List[Dict]:
        query = query.lower()
        results = self.index.get(query, [])
        return [{"url": url, "snippet": snippet} for url, snippet in results]
