import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.planner import plan_query_mcp
from agents.executors import summarize_abstracts
from agents.router import route_and_fetch
from utils.vector_store import search_similar, upsert_papers
from models.schemas import Paper, SummarizationRequest, Summary, RAGSummaryRequest
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/query_all", response_model=list[Paper])
def query_all(topic: str):
    plan = plan_query_mcp(topic)
    papers = route_and_fetch(plan)
    upsert_papers(papers)

    def safe_paper(p):
        return {
            "title": p.get("title", ""),
            "authors": p.get("authors", []),
            "abstract": p.get("abstract", ""),
            "published": p.get("published", ""),
            "url": p.get("url", ""),
            "source": p.get("source", "unknown")
        }

    sanitized = []
    for p in papers:
        if "abstract" in p and "title" in p:
            try:
                sanitized.append(safe_paper(p))
            except Exception as e:
                logging.warning(f"Skipping invalid paper: {e}")
    return sanitized

@app.get("/semantic_search")
def semantic_search(q: str):
    return search_similar(q)

@app.post("/rag_summarize", response_model=Summary)
def rag_summarize(request: RAGSummaryRequest):
    plan = plan_query_mcp(request.query)
    context = route_and_fetch(plan)

    def safe_paper(p):
        return {
            "title": p.get("title", ""),
            "authors": p.get("authors", []),
            "abstract": p.get("abstract", ""),
            "published": p.get("published", ""),
            "url": p.get("url", ""),
            "source": p.get("source", "unknown")
        }

    cleaned = [safe_paper(p) for p in context if "abstract" in p]
    abstracts = [p["abstract"] for p in cleaned]

    if not abstracts:
        return {"summary": "No relevant abstracts found."}

    return {"summary": summarize_abstracts(abstracts)}

@app.post("/summarize", response_model=Summary)
def summarize(request: SummarizationRequest):
    summary = summarize_abstracts(request.abstracts)
    return {"summary": summary}

@app.get("/plan")
def get_execution_plan(topic: str):
    return plan_query_mcp(topic).dict()