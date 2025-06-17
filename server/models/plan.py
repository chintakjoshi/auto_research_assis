from pydantic import BaseModel
from typing import Literal, List

class RetrievalTask(BaseModel):
    type: Literal["semantic", "keyword"]
    query: str
    sources: List[str]

class ExecutionPlan(BaseModel):
    steps: List[RetrievalTask]