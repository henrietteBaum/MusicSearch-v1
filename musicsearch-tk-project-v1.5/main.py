"""Entry point for tk-music-search application."""

import sys
from pathlib import Path

# Add src to path so imports work (src is a sibling directory of this file)
src_path = Path(__file__).parent / "src"
if not src_path.exists():
    raise RuntimeError(f"Expected src directory at {src_path!s} but it does not exist")
sys.path.insert(0, str(src_path))

from music_search.gui.main import App
from music_search.config import AppConfig

def main():
    """Run the application."""
    config = AppConfig()
    app = App(config)
    app.mainloop()


if __name__ == "__main__":
    main()
