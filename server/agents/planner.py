from models.plan import ExecutionPlan, RetrievalTask

def plan_query_mcp(topic: str) -> ExecutionPlan:
    return ExecutionPlan(steps=[
        RetrievalTask(type="keyword", query=topic, sources=["arxiv", "pubmed"]),
        RetrievalTask(type="semantic", query=topic, sources=["pinecone"])
    ])