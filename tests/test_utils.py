import io
import csv
from pubmed_pharma_fetcher.utils import export_papers_to_csv
from pubmed_pharma_fetcher.models import Paper, Author, Affiliation

def test_export_papers_to_csv(tmp_path):
    paper = Paper(
        pubmed_id="1",
        title="Test Title",
        publication_date="2024-01-01",
        authors=[Author(name="John Smith", affiliations=[Affiliation(name="Acme Biotech, Inc.")])],
        non_academic_authors=["John Smith"],
        company_affiliations=["Acme Biotech, Inc."],
        corresponding_author_email="john@acmebio.com"
    )
    file_path = tmp_path / "out.csv"
    export_papers_to_csv([paper], str(file_path))
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert rows[0] == [
            'PubmedID', 'Title', 'Publication Date',
            'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
        ]
        assert rows[1][0] == "1"
        assert rows[1][1] == "Test Title"
        assert rows[1][3] == "John Smith"
        assert rows[1][4] == "Acme Biotech, Inc."
        assert rows[1][5] == "john@acmebio.com" 