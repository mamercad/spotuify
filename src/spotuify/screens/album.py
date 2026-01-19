"""Album screen."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive

from ..widgets.track_list import TrackList
from ..utils.formatting import format_artist_names, format_duration


class AlbumScreen(Screen):
    """Screen for viewing an album's tracks."""

    DEFAULT_CSS = """
    AlbumScreen {
        layout: vertical;
    }

    AlbumScreen .album-header {
        height: auto;
        min-height: 5;
        padding: 1;
        background: $surface;
        border-bottom: solid $primary-darken-2;
    }

    AlbumScreen .album-title {
        text-style: bold;
        color: $text;
    }

    AlbumScreen .album-artist {
        color: $primary;
    }

    AlbumScreen .album-info {
        color: $text-muted;
    }

    AlbumScreen .album-content {
        height: 1fr;
        padding: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("enter", "play_selected", "Play"),
    ]

    album_id: reactive[str] = reactive("")
    album_data: reactive[dict[str, Any] | None] = reactive(None)

    def __init__(self, album_id: str = "") -> None:
        super().__init__()
        self.album_id = album_id

    def compose(self) -> ComposeResult:
        """Compose the album screen."""
        with Vertical(classes="album-header"):
            yield Label("Loading...", id="album-title", classes="album-title")
            yield Label("", id="album-artist", classes="album-artist")
            yield Label("", id="album-info", classes="album-info")

        with Vertical(classes="album-content"):
            yield TrackList(id="album-tracks")

    def on_mount(self) -> None:
        """Load album when mounted."""
        if self.album_id:
            self.load_album(self.album_id)

    def load_album(self, album_id: str) -> None:
        """Load album data."""
        self.album_id = album_id

        if hasattr(self.app, "spotify") and self.app.spotify:
            album = self.app.spotify.get_album(album_id)
            if album:
                self.album_data = album
                self._update_display()

    def _update_display(self) -> None:
        """Update the display with album data."""
        if not self.album_data:
            return

        # Update header
        title = self.query_one("#album-title", Label)
        title.update(self.album_data.get("name", "Unknown Album"))

        artist = self.query_one("#album-artist", Label)
        artists = format_artist_names(self.album_data.get("artists", []))
        artist.update(artists)

        info = self.query_one("#album-info", Label)
        release_date = self.album_data.get("release_date", "")[:4]
        total_tracks = self.album_data.get("total_tracks", 0)
        album_type = self.album_data.get("album_type", "album").capitalize()
        info.update(f"{album_type} • {release_date} • {total_tracks} tracks")

        # Load tracks - album tracks don't have the wrapper, so format them
        tracks_data = self.album_data.get("tracks", {}).get("items", [])
        # Add album info to each track for display purposes
        for track in tracks_data:
            track["album"] = {
                "name": self.album_data.get("name", ""),
                "images": self.album_data.get("images", []),
            }
            # Album tracks may not have full artist info
            if not track.get("artists"):
                track["artists"] = self.album_data.get("artists", [])

        track_list = self.query_one("#album-tracks", TrackList)
        track_list.set_tracks(
            tracks_data,
            context_uri=self.album_data.get("uri"),
            show_album=False,  # No need to show album name on album page
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
