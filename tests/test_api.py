import pytest
from pubmed_pharma_fetcher import api
from unittest.mock import patch

def test_search_pubmed_returns_ids():
    mock_response = {"esearchresult": {"idlist": ["123", "456"]}}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        ids = api.search_pubmed("test query")
        assert ids == ["123", "456"]

def test_fetch_pubmed_details_returns_xml():
    mock_xml = "<xml>data</xml>"
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_xml
        xml = api.fetch_pubmed_details(["123", "456"])
        assert xml == mock_xml
