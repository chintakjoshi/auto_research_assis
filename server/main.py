from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.planner import plan_query
from agents.executors import summarize_abstracts
from utils.arxiv_client import fetch_arxiv_papers
from utils.vector_store import search_similar
from utils.vector_store import upsert_papers
from models.schemas import Paper, SummarizationRequest, Summary
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/query", response_model=list[Paper])
def query_papers(topic: str = Query(..., description="Search topic or keywords")):
    sub_tasks = plan_query(topic)
    papers = fetch_arxiv_papers(sub_tasks["search_query"])
    upsert_papers([p.dict() for p in papers])
    return papers

@app.get("/semantic_search")
def semantic_search(q: str):
    return search_similar(q)

@app.post("/summarize", response_model=Summary)
def summarize(request: SummarizationRequest):
    summary = summarize_abstracts(request.abstracts)
    return {"summary": summary}