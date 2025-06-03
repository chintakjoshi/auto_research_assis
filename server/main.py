from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.planner import plan_query
from agents.executors import summarize_abstracts
from utils.arxiv_client import fetch_arxiv_papers
from utils.vector_store import search_similar, upsert_papers
from utils.pubmed_client import fetch_pubmed_papers
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
def query_all(topic: str = Query(..., description="Search topic or keywords")):
    sub_tasks = plan_query(topic)
    arxiv_papers = fetch_arxiv_papers(sub_tasks["search_query"])
    pubmed_papers = fetch_pubmed_papers(sub_tasks["search_query"])
    upsert_papers([p.dict() for p in arxiv_papers])
    upsert_papers([p.dict() for p in pubmed_papers])
    return arxiv_papers + pubmed_papers

@app.get("/semantic_search")
def semantic_search(q: str):
    return search_similar(q)

@app.post("/rag_summarize", response_model=Summary)
def rag_summarize(request: RAGSummaryRequest):
    matches = search_similar(request.query)
    abstracts = [m["abstract"] for m in matches if "abstract" in m]
    if not abstracts:
        return {"summary": "No relevant papers found."}
    summary = summarize_abstracts(abstracts)
    return {"summary": summary}

@app.post("/summarize", response_model=Summary)
def summarize(request: SummarizationRequest):
    summary = summarize_abstracts(request.abstracts)
    return {"summary": summary}