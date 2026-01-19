"""Playlist screen."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive

from ..widgets.track_list import TrackList
from ..utils.formatting import truncate_text


class PlaylistScreen(Screen):
    """Screen for viewing a playlist's tracks."""

    DEFAULT_CSS = """
    PlaylistScreen {
        layout: vertical;
    }

    PlaylistScreen .playlist-header {
        height: auto;
        min-height: 5;
        padding: 1;
        background: $surface;
        border-bottom: solid $primary-darken-2;
    }

    PlaylistScreen .playlist-title {
        text-style: bold;
        color: $text;
    }

    PlaylistScreen .playlist-info {
        color: $text-muted;
    }

    PlaylistScreen .playlist-description {
        color: $text-disabled;
        margin-top: 1;
    }

    PlaylistScreen .playlist-content {
        height: 1fr;
        padding: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("enter", "play_selected", "Play"),
    ]

    playlist_id: reactive[str] = reactive("")
    playlist_data: reactive[dict[str, Any] | None] = reactive(None)

    def __init__(self, playlist_id: str = "") -> None:
        super().__init__()
        self.playlist_id = playlist_id

    def compose(self) -> ComposeResult:
        """Compose the playlist screen."""
        with Vertical(classes="playlist-header"):
            yield Label("Loading...", id="playlist-title", classes="playlist-title")
            yield Label("", id="playlist-info", classes="playlist-info")
            yield Label("", id="playlist-description", classes="playlist-description")

        with Vertical(classes="playlist-content"):
            yield TrackList(id="playlist-tracks")

    def on_mount(self) -> None:
        """Load playlist when mounted."""
        if self.playlist_id:
            self.load_playlist(self.playlist_id)

    def load_playlist(self, playlist_id: str) -> None:
        """Load playlist data."""
        self.playlist_id = playlist_id

        if hasattr(self.app, "spotify") and self.app.spotify:
            playlist = self.app.spotify.get_playlist(playlist_id)
            if playlist:
                self.playlist_data = playlist
                self._update_display()

    def _update_display(self) -> None:
        """Update the display with playlist data."""
        if not self.playlist_data:
            return

        # Update header
        title = self.query_one("#playlist-title", Label)
        title.update(self.playlist_data.get("name", "Unknown Playlist"))

        info = self.query_one("#playlist-info", Label)
        owner = self.playlist_data.get("owner", {}).get("display_name", "Unknown")
        total = self.playlist_data.get("tracks", {}).get("total", 0)
        info.update(f"By {owner} • {total} tracks")

        description = self.query_one("#playlist-description", Label)
        desc_text = self.playlist_data.get("description", "")
        if desc_text:
            description.update(truncate_text(desc_text, 100))
        else:
            description.display = False

        # Load tracks
        tracks = self.playlist_data.get("tracks", {}).get("items", [])
        track_list = self.query_one("#playlist-tracks", TrackList)
        track_list.set_tracks(
            tracks,
            context_uri=self.playlist_data.get("uri"),
            show_added_at=True,
        )

    def on_track_list_track_selected(self, event: TrackList.TrackSelected) -> None:
        """Handle track selection."""
        if hasattr(self.app, "play_uri"):
            self.app.play_uri(
                event.track_uri,
                context_uri=event.context_uri,
                offset=event.index,
            )

    def action_go_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()
