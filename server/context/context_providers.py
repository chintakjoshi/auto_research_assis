from utils.arxiv_client import fetch_arxiv_papers
from utils.pubmed_client import fetch_pubmed_papers
from utils.vector_store import search_similar

def get_context_sources(query: str) -> list[dict]:
    arxiv = fetch_arxiv_papers(query)
    pubmed = fetch_pubmed_papers(query)
    return arxiv + pubmed

def get_semantic_context(query: str) -> list[dict]:
    return search_similar(query)