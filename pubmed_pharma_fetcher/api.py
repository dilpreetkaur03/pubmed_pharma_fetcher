import requests
from typing import List, Dict, Any
from .models import Paper

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

class PubMedAPIError(Exception):
    """Custom exception for PubMed API errors."""
    pass

def search_pubmed(query: str, retmax: int = 100) -> List[str]:
    """
    Search PubMed for a query and return a list of PubMed IDs.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    if response.status_code != 200:
        raise PubMedAPIError(f"PubMed search failed: {response.status_code}")
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_details(pubmed_ids: List[str]) -> str:
    """
    Fetch details for a list of PubMed IDs. Returns XML string.
    """
    if not pubmed_ids:
        return ""
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    if response.status_code != 200:
        raise PubMedAPIError(f"PubMed fetch failed: {response.status_code}")
    return response.text

# Parsing of XML to Paper objects will be handled in parser.py
