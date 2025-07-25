import pytest
from typer.testing import CliRunner
from cli import app
from unittest.mock import patch

runner = CliRunner()

def test_cli_runs_and_prints(monkeypatch):
    # Patch the API and parser to avoid real network calls
    with patch("pubmed_pharma_fetcher.api.search_pubmed", return_value=["1"]), \
         patch("pubmed_pharma_fetcher.api.fetch_pubmed_details", return_value="<xml></xml>"), \
         patch("pubmed_pharma_fetcher.parser.parse_pubmed_xml", return_value=[]), \
         patch("pubmed_pharma_fetcher.heuristics.apply_heuristics", return_value=[]):
        result = runner.invoke(app, ["test query"])
        assert result.exit_code == 0
        # Should not error, even if no results
