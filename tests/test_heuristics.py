from pubmed_pharma_fetcher.heuristics import is_non_academic_affiliation, extract_company_name, is_company_email, apply_heuristics
from pubmed_pharma_fetcher.models import Paper, Author, Affiliation

def test_is_non_academic_affiliation():
    assert is_non_academic_affiliation("Acme Biotech, Inc.")
    assert not is_non_academic_affiliation("Harvard University")
    assert is_non_academic_affiliation("Genmab US, Inc.")
    assert not is_non_academic_affiliation("Department of Medicine, University of Toronto")

def test_extract_company_name():
    assert extract_company_name("Acme Biotech, Inc.") == "Acme Biotech, Inc."
    assert extract_company_name("Harvard University") == ""

def test_is_company_email():
    assert is_company_email("john@acmebio.com")
    assert not is_company_email("jane@harvard.edu")
    assert is_company_email("someone@genmab.com")
    assert not is_company_email("test@university.edu")

def test_apply_heuristics_marks_non_academic():
    paper = Paper(
        pubmed_id="1",
        title="Test",
        publication_date="2024-01-01",
        authors=[
            Author(
                name="John Smith",
                affiliations=[Affiliation(name="Acme Biotech, Inc.")],
                email="john@acmebio.com"
            ),
            Author(
                name="Jane Doe",
                affiliations=[Affiliation(name="Harvard University")],
                email="jane@harvard.edu"
            )
        ],
        non_academic_authors=[],
        company_affiliations=[],
        corresponding_author_email=None
    )
    papers = apply_heuristics([paper])
    assert papers[0].non_academic_authors == ["John Smith"]
    assert "Acme Biotech, Inc." in papers[0].company_affiliations
    assert papers[0].corresponding_author_email == "john@acmebio.com"
