import pytest
from pubmed_pharma_fetcher import api
from unittest.mock import patch, MagicMock


def test_search_pubmed_returns_ids():
    mock_response = {"esearchresult": {"idlist": ["123", "456"]}}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        ids = api.search_pubmed("test query")
        assert ids == ["123", "456"]


def test_search_pubmed_no_idlist_key():
    mock_response = {"esearchresult": {}}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        ids = api.search_pubmed("test query")
        assert ids == []


def test_search_pubmed_no_esearchresult_key():
    mock_response = {}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        ids = api.search_pubmed("test query")
        assert ids == []


def test_search_pubmed_api_error():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        with pytest.raises(api.PubMedAPIError) as exc:
            api.search_pubmed("test query")
        assert "PubMed search failed: 500" in str(exc.value)


def test_search_pubmed_empty_idlist():
    mock_response = {"esearchresult": {"idlist": []}}
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        ids = api.search_pubmed("test query")
        assert ids == []


def test_search_pubmed_invalid_json_raises_exception():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("invalid json")
        with pytest.raises(ValueError):
            api.search_pubmed("test query")


def test_fetch_pubmed_details_returns_xml():
    mock_xml = "<xml>data</xml>"
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_xml
        xml = api.fetch_pubmed_details(["123", "456"])
        assert xml == mock_xml


def test_fetch_pubmed_details_api_error():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 503
        with pytest.raises(api.PubMedAPIError) as exc:
            api.fetch_pubmed_details(["123", "456"])
        assert "PubMed fetch failed: 503" in str(exc.value)


def test_fetch_pubmed_details_empty_list():
    xml = api.fetch_pubmed_details([])
    assert xml == ""
