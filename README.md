# Omni Search

This project is a **hybrid AI-powered search system** that:

- Searches through **local files** (PDF, DOCX, TXT).
- Scrapes the **web** for relevant results.
- Generates a combined **AI answer** using both sources.

## Features

- Local context search from your documents.
- Web scraping for up-to-date info.
- AI-powered answer synthesis.
- Modular Python codebase.

# Search engine

`searching/`

## Setup

1. Clone repo

   ```bash
   git clone https://github.com/harshith-ashok/omni_search.git
   cd omni_search/search_engine
   ```

2. Install dependencies

   ```bash
   source ./.search-env/bin/activate
   pip3 install -r ./req.txt
   ```

3. Start FastAPI server

   ```bash
   uvicorn main:app --reload
   ```

## Usage

1. Crawl URL(s)

   ```bash
   curl -X POST "http://127.0.0.1:8000/crawl" -H "Content-Type: application/json" -d '["https://harshithashok.com", "https://tailwindcss.com"]'
   ```

2. Search (Based on ranking)

   - Ranking is done using `scikit-learn` with the help of TF-IDF ranking

   ```bash
   curl "http://127.0.0.1:8000/search?query=fastapi&top_k=3
   ```

## Sample Response

```json
{
  "query": "tailwind",
  "results": [
    {
      "url": "https://tailwindcss.com",
      "score": 0.26542749569860913,
      "snippet": "Tailwind CSS - Rapidly build modern websites without ever leaving your HTML. v4.1 ⌘K Ctrl K Docs Blog Showcase Sponsor Plus text-4xl text-5xl text-6xl text-8xl text-gray-950 text-white tracking-tighter text-balance Rapidly build modern websites without ever leaving your HTML. text-lg text-gray-950 t"
    }
  ]
}
```

✨ Built with Python, AI, and curiosity.
