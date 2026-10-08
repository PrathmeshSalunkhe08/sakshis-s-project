# Concurrent Multi-Source News Scraper & LLM Summarizer

An asynchronous Python application that fetches news article content concurrently from multiple sources (`GNews`, `NewsData.io`, `Currents API`) using `asyncio` and `httpx`, validates data using **Pydantic**, extracts structured insights using **LangChain** with **Groq LLM** (`.with_structured_output()`), and exports results to `final_insights.json`.

---

## 🚀 Key Features

1. **Multi-Source Concurrent Fetching**: Uses `asyncio.gather()` and `httpx.AsyncClient` to hit multiple news APIs simultaneously.
2. **Robust Scraping & Error Handling**: Fetches webpage content concurrently and handles network timeouts, 404s, and invalid links gracefully.
3. **Pydantic Data Validation**:
   - `ArticleInput`: Validates fetched raw content and status.
   - `LLMArticleInsight`: Enforces strict data types for title, summary, topics, urgency score (`1` to `10`), and category (`Tech`, `Business`, `Health`, `Other`).
4. **LangChain Structured Output**: Uses Groq LLM with `.with_structured_output(LLMArticleInsight)` to produce clean, validated JSON outputs.

---

## 📁 Project Structure

```
news-ai-analyzer/
│
├── main.py                # Application orchestrator & async pipeline
├── models.py              # Pydantic data models (ArticleInput, LLMArticleInsight)
├── article_fetcher.py     # Asynchronous article content fetcher with error handling
├── llm_analyzer.py        # LangChain + Groq structured output analyzer
├── news_api.py            # Multi-API integrations (GNews, NewsData, Currents)
├── output.py              # Saves insights & exports to final_insights.json
├── final_insights.json    # Exported JSON output containing structured results
├── .env.example           # Example environment variables template
├── .gitignore             # Excludes .env, venv, and cache files from Git
├── README.md              # Documentation
├── pyproject.toml         # Project dependencies & package metadata
└── requirements.txt       # Dependencies list
```

---

## 🛠️ Setup & Local Execution Guide

### 1. Clone the Repository
```bash
git clone https://github.com/PrathmeshSalunkhe08/sakshis-s-project.git
cd sakshis-s-project
```

### 2. Set Up Virtual Environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the root folder (or copy from `.env.example`):
```bash
# Windows (CMD / PowerShell):
copy .env.example .env

# Mac / Linux:
cp .env.example .env
```

Open `.env` and insert your API keys:
```env
GNEWS_API_KEY=your_gnews_api_key
NEWS_API_KEY=your_newsdata_api_key
Current_NEWS_API=your_currents_api_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the Application
```bash
python main.py
```

---

## 📤 Output (`final_insights.json`)

The output is saved in `final_insights.json` containing structured analysis:

```json
[
    {
        "title": "Ray Dalio warns that AI is a classic bubble close to bursting",
        "summary": "Ray Dalio cautions that the rapid rise of AI has created a speculative bubble...",
        "topics": [
            "Artificial Intelligence",
            "Market Bubble",
            "Ray Dalio"
        ],
        "urgency_score": 8,
        "category": "Business"
    }
]
```
