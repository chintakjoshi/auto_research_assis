import os
from pinecone import Pinecone, ServerlessSpec
from models.schemas import Paper

from utils.embedder import embed_text

# Load env vars
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "").strip()
PINECONE_ENV = os.getenv("PINECONE_ENV", "").strip()
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "").strip()
PINECONE_DIM = 384  # adjust based on your embedding model

# Create Pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if it doesn't exist
if PINECONE_INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=PINECONE_DIM,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=PINECONE_ENV
        )
    )

# Connect to the index
index = pc.Index(PINECONE_INDEX_NAME)

def upsert_papers(papers: list[Paper | dict]):
    papers_dicts = [p.dict() if hasattr(p, "dict") else p for p in papers]
    texts = [p["abstract"] for p in papers_dicts]
    embeddings = embed_text(texts)
    vectors = [
        {
            "id": str(i),
            "values": emb,
            "metadata": {
                "title": p["title"],
                "abstract": p["abstract"],
                "published": p.get("published", ""),
                "url": p.get("url", "")
            },
        }
        for i, (emb, p) in enumerate(zip(embeddings, papers_dicts))
    ]
    index.upsert(vectors=vectors)


def search_similar(query: str, top_k=5) -> list[dict]:
    embedding = embed_text([query])[0]
    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return [match.metadata for match in results.matches]