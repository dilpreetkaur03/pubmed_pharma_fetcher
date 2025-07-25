import typer
from typing import Optional
from pubmed_pharma_fetcher.api import search_pubmed, fetch_pubmed_details, PubMedAPIError
from pubmed_pharma_fetcher.parser import parse_pubmed_xml
from pubmed_pharma_fetcher.heuristics import apply_heuristics
from pubmed_pharma_fetcher.utils import export_papers_to_csv, print_papers_table
from rich.console import Console

app = typer.Typer(help="Fetch PubMed papers with pharma/biotech authors.")

@app.command()
def get_papers_list(
    query: str = typer.Argument(..., help="PubMed search query (use quotes for complex queries)"),
    filename: Optional[str] = typer.Option(None, "-f", "--file", help="Filename to save results as CSV. If not provided, prints to console."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Print debug information during execution."),
):
    """
    Fetch PubMed papers with at least one non-academic (pharma/biotech) author.
    """
    console = Console()
    try:
        if debug:
            console.print(f"[bold blue]Searching PubMed for:[/bold blue] {query}")
        ids = search_pubmed(query)
        if debug:
            console.print(f"[bold blue]Found {len(ids)} PubMed IDs[/bold blue]")
        xml = fetch_pubmed_details(ids)
        if debug:
            console.print(f"[bold blue]Fetched XML for IDs[/bold blue]")
        papers = parse_pubmed_xml(xml)
        papers = apply_heuristics(papers)
        # Filter: Only papers with at least one non-academic author
        filtered = [p for p in papers if p.non_academic_authors]
        if debug:
            console.print(f"[bold blue]Filtered to {len(filtered)} papers with non-academic authors[/bold blue]")
        if filename:
            export_papers_to_csv(filtered, filename)
            console.print(f"[green]Results saved to {filename}[/green]")
        else:
            print_papers_table(filtered)
    except PubMedAPIError as e:
        console.print(f"[red]API Error:[/red] {e}")
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")

if __name__ == "__main__":
    app()
