# 🧠 Autonomous Research Assistant

A modular multi-agent system for real-time scientific literature discovery, semantic retrieval, and summarization. Built with FastAPI, LangChain, Pinecone, and DeepSeek LLM (via OpenRouter), this assistant supports intelligent workflows across arXiv and PubMed sources.

---

## 🚀 Features

- 🔍 **Multi-source Retrieval**: Searches arXiv and PubMed for scientific papers.
- 🧠 **Planner → Retriever → Summarizer** agents for modularity and interpretability.
- 📚 **Vector Search** with Pinecone for memory-augmented retrieval.
- 📄 **Summarization** of the most relevant abstracts using a custom LLM chain.
- 📈 **RAG Endpoint** for Retrieval-Augmented Generation summaries.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/auto_research_assis.git
cd auto_research_assis/server
```

### 2. Create and Activate Virtual Environment

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `server/` directory:

```env
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_API_KEY= api key
OPENAI_MODEL_NAME= model name
PINECONE_API_KEY= api key
PINECONE_ENV= region
PINECONE_INDEX_NAME=research-assistant-index
USER_EMAIL= email
```

### 5. Export Environment Variables (for Unix/macOS)

```bash
export $(cat .env | xargs)
```

---

## 🚦 Running the Server

```bash
uvicorn main:app --reload
```
## 🚦 Running the Client

```bash
npm run dev
```

---

## 🔌 API Endpoints

| Method | Endpoint                | Description                              |
|--------|-------------------------|------------------------------------------|
| GET    | `/query_all?topic=...`  | Search arXiv & PubMed for a topic        |
| GET    | `/semantic_search?q=...`| Vector-based abstract retrieval          |
| POST   | `/summarize`            | Summarize a list of abstracts            |
| POST   | `/rag_summarize`        | Summarize top matches from vector search |
| GET    | `/agent_summary`        | Run full agent pipeline                  |

---
