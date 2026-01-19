"""Sidebar navigation widget."""

from typing import Any
from textual.app import ComposeResult
from textual.widgets import Static, Label, ListItem, ListView
from textual.containers import Vertical, VerticalScroll
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text


class SidebarItem(ListItem):
    """A single item in the sidebar."""

    def __init__(
        self,
        label: str,
        item_id: str,
        icon: str = "",
        item_type: str = "nav",
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self.label_text = label
        self.item_id = item_id
        self.icon = icon
        self.item_type = item_type
        self.data = data or {}

    def compose(self) -> ComposeResult:
        """Compose the list item."""
        text = f"{self.icon} {self.label_text}" if self.icon else self.label_text
        yield Label(text)


class Sidebar(Static):
    """Sidebar navigation widget with playlists and library access."""

    DEFAULT_CSS = """
    Sidebar {
        width: 30;
        height: 100%;
        dock: left;
        background: $surface;
        border-right: solid $primary-darken-2;
    }

    Sidebar .sidebar-section {
        height: auto;
        padding: 1;
    }

    Sidebar .section-title {
        text-style: bold;
        color: $text-muted;
        padding: 0 0 1 0;
    }

    Sidebar ListView {
        height: auto;
        max-height: 20;
        background: transparent;
    }

    Sidebar ListView:focus {
        background: transparent;
    }

    Sidebar ListItem {
        padding: 0 1;
        height: 1;
    }

    Sidebar ListItem:hover {
        background: $surface-lighten-1;
    }

    Sidebar ListItem.-active {
        background: $primary-darken-1;
    }

    Sidebar .playlists-section {
        height: 1fr;
    }

    Sidebar .playlists-section ListView {
        max-height: 100%;
        height: 1fr;
    }
    """

    playlists: reactive[list[dict[str, Any]]] = reactive(list)

    def compose(self) -> ComposeResult:
        """Compose the sidebar layout."""
        # Navigation section
        with Vertical(classes="sidebar-section"):
            yield Label("Menu", classes="section-title")
            yield ListView(
                SidebarItem("Home", "home", "⌂", "nav"),
                SidebarItem("Search", "search", "○", "nav"),
                SidebarItem("Library", "library", "▤", "nav"),
                SidebarItem("Recently Played", "recent", "◷", "nav"),
                SidebarItem("Devices", "devices", "▣", "nav"),
                id="nav-list",
            )

        # Library section
        with Vertical(classes="sidebar-section"):
            yield Label("Your Library", classes="section-title")
            yield ListView(
                SidebarItem("Liked Songs", "liked", "♡", "library"),
                SidebarItem("Saved Albums", "albums", "◉", "library"),
                SidebarItem("Following", "artists", "☆", "library"),
                id="library-list",
            )

        # Playlists section
        with Vertical(classes="sidebar-section playlists-section"):
            yield Label("Playlists", classes="section-title")
            yield ListView(id="playlists-list")

    def set_playlists(self, playlists: list[dict[str, Any]]) -> None:
        """Set the playlists to display."""
        self.playlists = playlists
        self._update_playlists()

    def _update_playlists(self) -> None:
        """Update the playlists list."""
        playlist_list = self.query_one("#playlists-list", ListView)
        playlist_list.clear()

        for playlist in self.playlists:
            item = SidebarItem(
                label=playlist.get("name", "Unknown Playlist"),
                item_id=playlist.get("id", ""),
                icon="🎵",
                item_type="playlist",
                data=playlist,
            )
            playlist_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selection in any list view."""
        item = event.item
        if isinstance(item, SidebarItem):
            self.post_message(
                self.ItemSelected(
                    item_id=item.item_id,
                    item_type=item.item_type,
                    data=item.data,
                )
            )

    class ItemSelected(Message):
        """Message posted when a sidebar item is selected."""

        def __init__(
            self, item_id: str, item_type: str, data: dict[str, Any] | None = None
        ) -> None:
            self.item_id = item_id
            self.item_type = item_type
            self.data = data or {}
            super().__init__()
