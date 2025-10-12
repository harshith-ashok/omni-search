# Omni Search

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Java](https://img.shields.io/badge/Java-17%2B-orange?logo=java&logoColor=white)](https://www.oracle.com/java/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009485?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2%2B-6DB33F?logo=springboot&logoColor=white)](https://spring.io/projects/spring-boot)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)

This project is a **hybrid AI-powered search system** that:
- Searches through **local files** (PDF, DOCX, TXT, etc.)
- Scrapes the **web** for relevant results
- Generates a combined **AI answer** using both sources
- Offers both **Python** and **Java** implementations

## Features

✨ **Core Features:**
- Local context search from your documents
- Web scraping for up-to-date information
- AI-powered answer synthesis
- Multi-language support (Python & Java)
- REST API endpoints
- Session-based chat history
- TF-IDF based ranking for search results

---

# Python Implementation

## Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/harshith-ashok/omni_search.git
   cd omni_search/searching
   ```

2. Create and activate virtual environment
   ```bash
   python3 -m venv .search-env
   source .search-env/bin/activate  # On Windows: .search-env\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`

## API Endpoints

### 1. **Local File Search**
Search for files in your system directories.

```bash
curl "http://127.0.0.1:8000/local?query=.js"
```

**Response:**
```json
{
  "results": [
    {
      "folder": "Documents",
      "file": "script.js"
    }
  ]
}
```

### 2. **Deep Local Search**
Recursively search through subdirectories (up to 4 levels deep).

```bash
curl "http://127.0.0.1:8000/local-deep?query=.pdf"
```

**Response:**
```json
{
  "results": [
    {
      "folder": "Downloads",
      "subfolder": "Research/Papers",
      "file": "paper.pdf"
    }
  ]
}
```

### 3. **Web Crawling & Indexing**
Crawl a website and build a searchable index.

```bash
curl -X POST "http://127.0.0.1:8000/index?start_url=https://example.com&max_pages=5"
```

**Response:**
```json
{
  "indexed": 5,
  "data": [
    {
      "url": "https://example.com",
      "title": "Example Domain",
      "snippet": "This domain is for use in examples and educational..."
    }
  ]
}
```

### 4. **Search Indexed Content**
Search through previously indexed websites.

```bash
curl "http://127.0.0.1:8000/search?query=example"
```

**Response:**
```json
{
  "query": "example",
  "results": [
    {
      "url": "https://example.com",
      "title": "Example Domain",
      "snippet": "This domain is for use in examples..."
    }
  ]
}
```

### 5. **DuckDuckGo Search**
Perform real-time web searches using DuckDuckGo.

```bash
curl "http://127.0.0.1:8000/gquery?query=fastapi&num_results=5"
```

**Response:**
```json
{
  "query": "fastapi",
  "results": [
    {
      "title": "FastAPI",
      "url": "https://fastapi.tiangolo.com/",
      "snippet": "FastAPI is a modern, fast web framework for building APIs..."
    }
  ]
}
```

### 6. **AI Chat with LLM**
Chat with a local LLM (requires Ollama running locally).

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"session_id": "user123", "message": "Tell me about FastAPI"}'
```

**Response:**
```json
{
  "reply": "FastAPI is a modern Python web framework for building APIs..."
}
```

## Configuration

Edit `main.py` to customize:
- Search folders: Modify the `LIST` variable
- Home directory: Change the `HOME` variable
- LLM model: Update in `llm.py`

---

# Java Implementation

## Setup

### Prerequisites
- Java 17 or higher
- Maven 3.6 or higher

### Installation

1. Navigate to the Java project directory
   ```bash
   cd baymax-chatbot
   ```

2. Install dependencies and build
   ```bash
   mvn clean install
   ```

### Running the Server

**Option 1: Using Maven**
```bash
mvn spring-boot:run
```

**Option 2: Running JAR file**
```bash
mvn clean package
java -jar target/baymax-chatbot-1.0.0.jar
```

The server will be available at `http://127.0.0.1:8000`

## API Endpoints

All Java endpoints mirror the Python implementation exactly. The JSON responses are identical.

### 1. **Local File Search**
```bash
curl "http://127.0.0.1:8000/local?query=.js"
```

### 2. **Deep Local Search**
```bash
curl "http://127.0.0.1:8000/local-deep?query=.pdf"
```

### 3. **Web Crawling & Indexing**
```bash
curl -X POST "http://127.0.0.1:8000/index?start_url=https://example.com&max_pages=5"
```

### 4. **Search Indexed Content**
```bash
curl "http://127.0.0.1:8000/search?query=example"
```

### 5. **DuckDuckGo Search**
```bash
curl "http://127.0.0.1:8000/gquery?query=fastapi&num_results=5"
```

### 6. **AI Chat with LLM**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"session_id": "user123", "message": "Tell me about FastAPI"}'
```

## Project Structure

See the main repository for directory organization.

---

## Dependencies

**Java Libraries:**
- Spring Boot 3.2.0 - Web framework
- jsoup 1.17.2 - HTML parsing & web scraping
- Gson 2.10.1 - JSON processing
- Apache HttpClient 5.3 - HTTP requests
- Maven 3.6+ - Build management

**Python Libraries:**
- FastAPI - Web framework
- BeautifulSoup4 - Web scraping
- Requests - HTTP library
- Scikit-learn - TF-IDF ranking
- Ollama - Local LLM integration

## Configuration

**Java (application.properties):**
```properties
server.port=8000
spring.application.name=Baymax Chatbot
```

**LLM Settings (BaymaxChat.java):**
```java
this.model = "llama3.2";
this.host = "http://localhost:11434";  // Ollama endpoint
```

## Requirements

### For LLM Integration
You need to have Ollama running locally:
1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull llama3.2`
3. Start Ollama: `ollama serve`

The default port is `localhost:11434`

---

## Comparison: Python vs Java

| Feature | Python | Java |
|---------|--------|------|
| Framework | FastAPI | Spring Boot |
| Port | 8000 | 8000 |
| Web Scraping | BeautifulSoup | jsoup |
| JSON Handling | Built-in | Gson |
| API Response | Identical | Identical |
| LLM Integration | Ollama | Ollama |
| Setup Time | 5 minutes | 10 minutes |
| Memory Usage | Lower | Higher |
| Performance | Good | Better |
| Scalability | Medium | High |

## Usage Example

### Python
```bash
# Start server
uvicorn main:app --reload

# Search the web
curl "http://127.0.0.1:8000/gquery?query=python%20rest%20api&num_results=5"
```

### Java
```bash
# Start server
mvn spring-boot:run

# Search the web (same endpoint, same response)
curl "http://127.0.0.1:8000/gquery?query=python%20rest%20api&num_results=5"
```

---

## Sample API Responses

### Search Results
```json
{
  "query": "tailwind css",
  "results": [
    {
      "url": "https://tailwindcss.com",
      "title": "Tailwind CSS",
      "snippet": "Rapidly build modern websites without ever leaving your HTML..."
    },
    {
      "url": "https://tailwindcss.com/docs",
      "title": "Tailwind CSS Documentation",
      "snippet": "Learn how to use Tailwind CSS to build custom designs..."
    }
  ]
}
```

### Chat Response
```json
{
  "reply": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints. The key features are: Very fast, Automatic interactive API documentation, Easy to use..."
}
```

---

## Troubleshooting

### Python
**Issue:** `ModuleNotFoundError: No module named 'fastapi'`
- Solution: Activate venv and run `pip install -r requirements.txt`

**Issue:** LLM not responding
- Solution: Ensure Ollama is running with `ollama serve`

### Java
**Issue:** `Main class not found`
- Solution: Rebuild with `mvn clean install`

**Issue:** Port already in use
- Solution: Change port in `application.properties` or kill process on 8000

**Issue:** Compilation errors
- Solution: Ensure Java 17+ is installed: `java -version`

---

## Contributing

Contributions are welcome! Feel free to:
- Add more search backends
- Improve ranking algorithms
- Add authentication
- Optimize performance
- Fix bugs

---

## License

MIT License - Feel free to use this project for personal or commercial purposes.

---

## Built With

Python: FastAPI, BeautifulSoup, Scikit-learn, Ollama
Java: Spring Boot, jsoup, Gson, Apache HttpClient
AI: Ollama with llama3.2

Built with Python, Java, AI, and curiosity.