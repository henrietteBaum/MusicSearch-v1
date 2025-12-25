"""Tests for iTunes API."""

import pytest
from music_search.api.itunes import ITunesAPI


class TestITunesAPI:
    """Test suite for ITunesAPI class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.api = ITunesAPI()

    def test_api_init(self):
        """Test API initialization."""
        assert self.api.base_url == "https://itunes.apple.com/search"
        assert self.api.timeout == 10

    def test_search_empty_term_raises_error(self):
        """Test that empty search term raises ValueError."""
        with pytest.raises(ValueError, match="Search term cannot be empty"):
            self.api.search("")

    def test_search_invalid_limit_raises_error(self):
        """Test that invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="Invalid limit"):
            self.api.search("test", limit="invalid")

    def test_format_results_empty(self):
        """Test formatting empty results."""
        data = {"resultCount": 0, "results": []}
        formatted = self.api.format_results(data)
        assert formatted == ["No results found."]

    def test_format_results_with_data(self):
        """Test formatting results with data."""
        data = {
            "resultCount": 1,
            "results": [
                {
                    "artistName": "The Beatles",
                    "collectionName": "Abbey Road",
                    "trackCount": 17,
                }
            ],
        }
        formatted = self.api.format_results(data)
        assert len(formatted) == 2
        assert "Results found: 1" in formatted[0]
        assert "The Beatles" in formatted[1]
