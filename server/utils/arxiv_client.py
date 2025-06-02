import arxiv
from models.schemas import Paper

def fetch_arxiv_papers(query: str, max_results: int = 5) -> list[Paper]:
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for result in search.results():
        results.append(Paper(
            title=result.title,
            authors=[a.name for a in result.authors],
            abstract=result.summary,
            published=str(result.published),
            url=result.entry_id
        ))
    return results