from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TfidfIndexer:
    def __init__(self):
        self.documents = []      # list of texts
        self.urls = []           # list of URLs
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = None

    def add_document(self, url: str, text: str):
        self.urls.append(url)
        self.documents.append(text)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if not self.documents:
            return []

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        ranked_indices = scores.argsort()[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            if scores[idx] > 0:  # ignore irrelevant docs
                snippet = self.documents[idx][:300]
                results.append({
                    "url": self.urls[idx],
                    "score": float(scores[idx]),
                    "snippet": snippet
                })
        return results
