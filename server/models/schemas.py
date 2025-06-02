from pydantic import BaseModel
from typing import List

class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    published: str
    url: str

class SummarizationRequest(BaseModel):
    abstracts: List[str]

class Summary(BaseModel):
    summary: str