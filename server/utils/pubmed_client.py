import os
import httpx
from models.schemas import Paper
from typing import List
import xml.etree.ElementTree as ET

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_EMAIL = os.getenv("USER_EMAIL", "").strip()  # REQUIRED per NCBI's rules

def fetch_pubmed_papers(query: str, max_results: int = 5) -> List[Paper]:
    search_url = f"{NCBI_BASE}/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "email": USER_EMAIL
    }

    with httpx.Client(timeout=10) as client:
        search_resp = client.get(search_url, params=search_params)
        search_resp.raise_for_status()
        id_list = search_resp.json()["esearchresult"].get("idlist", [])

        if not id_list:
            return []

        # Step 2: Fetch abstracts for those IDs
        fetch_url = f"{NCBI_BASE}/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
            "email": USER_EMAIL
        }

        fetch_resp = client.get(fetch_url, params=fetch_params)
        fetch_resp.raise_for_status()
        root = ET.fromstring(fetch_resp.content)

        papers = []
        for article in root.findall(".//PubmedArticle"):
            try:
                article_title = article.findtext(".//ArticleTitle", default="")
                abstract_parts = article.findall(".//AbstractText")
                abstract = " ".join(a.text or "" for a in abstract_parts)

                authors = []
                for a in article.findall(".//Author"):
                    lname = a.findtext("LastName")
                    fname = a.findtext("ForeName")
                    if lname and fname:
                        authors.append(f"{fname} {lname}")

                pub_date = article.findtext(".//PubDate/Year", default="Unknown")
                pmid = article.findtext(".//PMID", default="0")
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"

                papers.append(Paper(
                    title=article_title,
                    authors=authors,
                    abstract=abstract,
                    published=pub_date,
                    url=url,
                    source="PubMed"
                ))

            except Exception:
                continue

    return papers