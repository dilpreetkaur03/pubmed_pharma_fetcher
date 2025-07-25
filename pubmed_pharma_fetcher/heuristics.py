from typing import List
from .models import Paper, Author, Affiliation

# Common keywords for non-academic/company affiliations
COMPANY_KEYWORDS = [
    'pharma', 'biotech', 'inc', 'ltd', 'llc', 'gmbh', 'corp', 'company', 'therapeutics', 'laboratories', 'industries', 'solutions', 'biosciences', 'genomics', 'diagnostics', 'medicines', 'healthcare', 'research institute', 'research center', 'research centre', 'clinic', 'hospital', 'medicinal', 'medical', 'devices', 'technology', 'technologies', 'systems', 'consulting', 'consultants', 'ventures', 'holdings', 'group', 's.a.', 's.r.l.', 'pvt', 'plc', 'co.', 's.p.a.'
]
ACADEMIC_KEYWORDS = [
    'university', 'college', 'school', 'institute of technology', 'faculty', 'department', 'academy', 'universität', 'universidade', 'università', 'universidad', 'universite', 'hochschule', 'polytechnic', 'centre for', 'center for', 'graduate', 'postgraduate', 'education', 'student', 'professor', 'prof.', 'phd', 'msc', 'bsc', 'md', 'hospital', 'clinic', 'children\'s hospital', 'medical center', 'med school', 'school of', 'faculty of', 'institute of', 'department of', 'division of', 'section of', 'univ.', 'dept.'
]

COMPANY_EMAIL_DOMAINS = [
    'com', 'co', 'biz', 'pharma', 'bio', 'med', 'health', 'corp', 'inc', 'ltd', 'llc', 'gmbh', 'solutions', 'systems', 'group', 'ventures', 'holdings', 'plc', 'srl', 'spa'
]


def is_non_academic_affiliation(affiliation: str) -> bool:
    affil_lower = affiliation.lower()
    # If it contains academic keywords, it's academic
    if any(word in affil_lower for word in ACADEMIC_KEYWORDS):
        return False
    # If it contains company keywords, it's non-academic
    if any(word in affil_lower for word in COMPANY_KEYWORDS):
        return True
    return False

def extract_company_name(affiliation: str) -> str:
    affil_lower = affiliation.lower()
    for word in COMPANY_KEYWORDS:
        if word in affil_lower:
            return affiliation
    return ''

def is_company_email(email: str) -> bool:
    if not email or '@' not in email:
        return False
    domain = email.split('@')[-1].lower()
    tld = domain.split('.')[-1]
    return tld in COMPANY_EMAIL_DOMAINS

def apply_heuristics(papers: List[Paper]) -> List[Paper]:
    """
    Update Paper objects in-place with non-academic author and company affiliation info.
    """
    for paper in papers:
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None
        for author in paper.authors:
            # Check all affiliations for non-academic/company
            for aff in author.affiliations:
                if is_non_academic_affiliation(aff.name):
                    aff.is_non_academic = True
                    company = extract_company_name(aff.name)
                    if company:
                        aff.company_name = company
                        author.company_affiliation = company
                        if company not in company_affiliations:
                            company_affiliations.append(company)
                    author.is_non_academic = True
            # Check email domain
            if author.email and is_company_email(author.email):
                author.is_non_academic = True
            if author.is_non_academic:
                non_academic_authors.append(author.name)
            # Try to set corresponding author email (first found)
            if not corresponding_email and author.email:
                corresponding_email = author.email
        paper.non_academic_authors = non_academic_authors
        paper.company_affiliations = company_affiliations
        paper.corresponding_author_email = corresponding_email
    return papers
