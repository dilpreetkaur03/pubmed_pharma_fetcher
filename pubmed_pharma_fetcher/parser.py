import xml.etree.ElementTree as ET
from typing import List
from .models import Paper, Author, Affiliation
import re

def is_likely_valid_email(email: str) -> bool:
    # Basic check: contains @, no spaces, doesn't end with a period, and has at least one dot after @
    if not email or '@' not in email or ' ' in email or email.endswith('.'):
        return False
    local, _, domain = email.rpartition('@')
    if '.' not in domain:
        return False
    return True

def parse_pubmed_xml(xml_data: str) -> List[Paper]:
    """
    Parse PubMed XML data and return a list of Paper objects.
    """
    if not xml_data.strip():
        return []
    root = ET.fromstring(xml_data)
    papers: List[Paper] = []
    for article in root.findall('.//PubmedArticle'):
        # Extract PubmedID
        pmid_elem = article.find('.//PMID')
        pubmed_id = pmid_elem.text if pmid_elem is not None else ''
        # Extract Title
        title_elem = article.find('.//ArticleTitle')
        title = title_elem.text if (title_elem is not None and title_elem.text is not None) else ''
        # Extract Publication Date
        date_elem = article.find('.//PubDate')
        if date_elem is not None:
            year = date_elem.findtext('Year', default='')
            month = date_elem.findtext('Month', default='')
            day = date_elem.findtext('Day', default='')
            publication_date = f"{year}-{month}-{day}".strip('-')
        else:
            publication_date = ''
        # Extract Authors
        authors: List[Author] = []
        non_academic_authors: List[str] = []
        company_affiliations: List[str] = []
        corresponding_author_email = None
        for author_elem in article.findall('.//Author'):
            name = ' '.join(filter(None, [
                author_elem.findtext('ForeName', ''),
                author_elem.findtext('LastName', '')
            ])).strip()
            affiliations: List[Affiliation] = []
            is_non_academic = False
            company_name = None
            email = None
            for aff_elem in author_elem.findall('.//AffiliationInfo/Affiliation'):
                aff_text = aff_elem.text or ''
                # Email extraction (simple heuristic)
                possible_email = None
                for word in aff_text.split():
                    if '@' in word:
                        possible_email = word.strip('.,;:()[]<>"\'')
                        break
                if possible_email and is_likely_valid_email(possible_email):
                    email = possible_email
                affiliations.append(Affiliation(name=aff_text))
            author = Author(
                name=name,
                affiliations=affiliations,
                email=email,
                is_non_academic=is_non_academic,
                company_affiliation=company_name
            )
            authors.append(author)
        paper = Paper(
            pubmed_id=pubmed_id,
            title=title,
            publication_date=publication_date,
            authors=authors,
            non_academic_authors=non_academic_authors,
            company_affiliations=company_affiliations,
            corresponding_author_email=corresponding_author_email
        )
        papers.append(paper)
    return papers
