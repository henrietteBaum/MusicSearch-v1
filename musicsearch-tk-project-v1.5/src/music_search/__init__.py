"""
Music Search Application - Tk-based GUI for searching music via iTunes API.

A learning project demonstrating:
- Clean project structure (src layout)
- Separation of concerns (GUI, API, Utils)
- Python best practices (type hints, docstrings, etc.)
"""

__version__ = "0.5.0"
__author__ = "Henriette Baum"

from .api.itunes import ITunesAPI
from .config import AppConfig

__all__ = ["ITunesAPI", "AppConfig"]
