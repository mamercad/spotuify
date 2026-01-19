"""Search bar widget."""

from textual.app import ComposeResult
from textual.widgets import Static, Input
from textual.containers import Horizontal
from textual.message import Message


class SearchBar(Static):
    """Search input widget."""

    DEFAULT_CSS = """
    SearchBar {
        height: 3;
        padding: 0 1;
    }

    SearchBar Horizontal {
        height: 3;
        align: left middle;
    }

    SearchBar Input {
        width: 100%;
        margin: 0;
    }

    SearchBar Input:focus {
        border: tall $primary;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        with Horizontal():
            yield Input(
                placeholder="🔍 Search for tracks, albums, artists, or playlists...",
                id="search-input",
            )

    def focus_search(self) -> None:
        """Focus the search input."""
        self.query_one("#search-input", Input).focus()

    def clear_search(self) -> None:
        """Clear the search input."""
        self.query_one("#search-input", Input).value = ""

    def get_query(self) -> str:
        """Get the current search query."""
        return self.query_one("#search-input", Input).value

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search submission."""
        query = event.value.strip()
        if query:
            self.post_message(self.SearchSubmitted(query))

    class SearchSubmitted(Message):
        """Message posted when search is submitted."""

        def __init__(self, query: str) -> None:
            self.query = query
            super().__init__()
