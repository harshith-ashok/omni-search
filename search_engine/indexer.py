import json
from crawler import WebCrawler


class Indexer:
    def __init__(self, index_file="index.json"):
        self.index_file = index_file

    def build_index(self, start_url, max_pages=10):
        crawler = WebCrawler(max_pages=max_pages)
        data = crawler.crawl(start_url=start_url)

        try:
            with open(self.index_file, "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_data.extend(data)

        with open(self.index_file, "w") as f:
            json.dump(existing_data, f, indent=2)

        return data

    def search_index(self, keyword):
        try:
            with open(self.index_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        results = []
        for entry in data:
            if keyword.lower() in entry["title"].lower() or keyword.lower() in entry["snippet"].lower():
                results.append(entry)

        return results
