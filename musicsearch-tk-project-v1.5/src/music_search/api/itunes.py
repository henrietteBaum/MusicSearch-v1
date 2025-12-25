"""iTunes API client for searching albums."""

from typing import Optional, Dict, List, Any
import requests
from ..utils.constants import ITUNES_API_URL, MAX_RESULTS


class ITunesAPI:
    """Client for iTunes API searches."""

    def __init__(self, timeout: int = 10):
        """
        Initialize iTunes API client.

        Args:
            timeout: Request timeout in seconds.
        """
        self.base_url = ITUNES_API_URL
        self.timeout = timeout

    def search(
        self, term: str, limit: Optional[int] = None, entity: str = "album"
    ) -> Dict[str, Any]:
        """
        Search iTunes for albums.

        Args:
            term: Search term (artist or album name).
            limit: Max results (None='all', uses MAX_RESULTS).
            entity: Entity type to search ('album', 'song', etc.).

        Returns:
            Dictionary with search results and metadata.

        Raises:
            requests.RequestException: If API request fails.
        """
        if not term or not term.strip():
            raise ValueError("Search term cannot be empty")

        # Handle 'all' or None -> use max
        if limit is None or limit == "all":
            limit = MAX_RESULTS
        elif isinstance(limit, str):
            try:
                limit = int(limit)
            except ValueError:
                raise ValueError(f"Invalid limit: {limit}")

        if limit < 1:
            raise ValueError("Limit must be >= 1")

        params = {"term": term.strip(), "entity": entity, "limit": limit}

        try:
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"iTunes API request failed: {str(e)}")

    def format_results(self, data: Dict[str, Any]) -> List[str]:
        """
        Format API response into readable strings.

        Args:
            data: Response from iTunes API.

        Returns:
            List of formatted result strings.
        """
        result_count = data.get("resultCount", 0)
        results = data.get("results", [])

        if not results:
            return ["No results found."]

        formatted = [f"Results found: {result_count}\n"]
        for result in results:
            artist = result.get("artistName", "Unknown")
            album = result.get("collectionName", "Unknown")
            tracks = result.get("trackCount", "?")
            formatted.append(f"{artist} – {album} (Tracks: {tracks})")

        return formatted
