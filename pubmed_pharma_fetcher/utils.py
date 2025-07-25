import csv
from typing import List, Optional
from .models import Paper
from rich.console import Console
from rich.table import Table

def export_papers_to_csv(papers: List[Paper], filename: str) -> None:
    """
    Export a list of Paper objects to a CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'PubmedID', 'Title', 'Publication Date',
            'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
        ])
        for paper in papers:
            writer.writerow([
                paper.pubmed_id,
                paper.title,
                paper.publication_date,
                '; '.join(paper.non_academic_authors),
                '; '.join(paper.company_affiliations),
                paper.corresponding_author_email or ''
            ])

def print_papers_table(papers: List[Paper]) -> None:
    """
    Pretty-print a list of Paper objects to the console using rich.
    """
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("PubmedID", style="dim", width=12)
    table.add_column("Title", width=40)
    table.add_column("Publication Date", width=12)
    table.add_column("Non-academic Author(s)", width=20)
    table.add_column("Company Affiliation(s)", width=20)
    table.add_column("Corresponding Author Email", width=25)
    for paper in papers:
        table.add_row(
            paper.pubmed_id,
            paper.title[:40] + ("..." if len(paper.title) > 40 else ""),
            paper.publication_date,
            '; '.join(paper.non_academic_authors),
            '; '.join(paper.company_affiliations),
            paper.corresponding_author_email or ''
        )
    console.print(table)
