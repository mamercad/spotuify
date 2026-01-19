"""Artist screen."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label, DataTable
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive

from ..widgets.track_list import TrackList
from ..utils.formatting import format_duration, format_play_count, truncate_text


class ArtistScreen(Screen):
    """Screen for viewing an artist's top tracks and albums."""

    DEFAULT_CSS = """
    ArtistScreen {
        layout: vertical;
    }

    ArtistScreen .artist-header {
        height: auto;
        min-height: 5;
        padding: 1;
        background: $surface;
        border-bottom: solid $primary-darken-2;
    }

    ArtistScreen .artist-name {
        text-style: bold;
        color: $text;
    }

    ArtistScreen .artist-info {
        color: $text-muted;
    }

    ArtistScreen .artist-genres {
        color: $text-disabled;
    }

    ArtistScreen .artist-content {
        height: 1fr;
        padding: 1;
    }

    ArtistScreen .section-title {
        text-style: bold;
        color: $text;
        padding: 1 0;
    }

    ArtistScreen .top-tracks {
        height: 40%;
        min-height: 10;
    }

    ArtistScreen .albums-section {
        height: 1fr;
    }

    ArtistScreen DataTable {
        height: 100%;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    artist_id: reactive[str] = reactive("")
    artist_data: reactive[dict[str, Any] | None] = reactive(None)
    top_tracks: reactive[list[dict[str, Any]]] = reactive(list)
    albums: reactive[list[dict[str, Any]]] = reactive(list)

    def __init__(self, artist_id: str = "") -> None:
        super().__init__()
        self.artist_id = artist_id

    def compose(self) -> ComposeResult:
        """Compose the artist screen."""
        with Vertical(classes="artist-header"):
            yield Label("Loading...", id="artist-name", classes="artist-name")
            yield Label("", id="artist-info", classes="artist-info")
            yield Label("", id="artist-genres", classes="artist-genres")

        with Vertical(classes="artist-content"):
            with Vertical(classes="top-tracks"):
                yield Label("Popular Tracks", classes="section-title")
                yield TrackList(id="artist-top-tracks")

            with Vertical(classes="albums-section"):
                yield Label("Albums", classes="section-title")
                yield DataTable(id="artist-albums", cursor_type="row")

    def on_mount(self) -> None:
        """Initialize and load artist data."""
        # Setup albums table
        albums_table = self.query_one("#artist-albums", DataTable)
        albums_table.add_column("Album", width=40, key="name")
        albums_table.add_column("Year", width=6, key="year")
        albums_table.add_column("Type", width=12, key="type")
        albums_table.add_column("Tracks", width=8, key="tracks")

        if self.artist_id:
            self.load_artist(self.artist_id)

    def load_artist(self, artist_id: str) -> None:
        """Load artist data."""
        self.artist_id = artist_id

        if hasattr(self.app, "spotify") and self.app.spotify:
            artist = self.app.spotify.get_artist(artist_id)
            if artist:
                self.artist_data = artist

            top_tracks = self.app.spotify.get_artist_top_tracks(artist_id)
            self.top_tracks = top_tracks

            albums_result = self.app.spotify.get_artist_albums(artist_id)
            self.albums = albums_result.get("items", [])

            self._update_display()

    def _update_display(self) -> None:
        """Update the display with artist data."""
        if not self.artist_data:
            return

        # Update header
        name = self.query_one("#artist-name", Label)
        name.update(self.artist_data.get("name", "Unknown Artist"))

        info = self.query_one("#artist-info", Label)
        followers = self.artist_data.get("followers", {}).get("total", 0)
        info.update(f"{followers:,} followers")

        genres = self.query_one("#artist-genres", Label)
        genre_list = self.artist_data.get("genres", [])
        if genre_list:
            genres.update(", ".join(genre_list[:5]))
        else:
            genres.display = False

        # Update top tracks
        track_list = self.query_one("#artist-top-tracks", TrackList)
        # Format tracks for TrackList
        formatted_tracks = [{"track": t} for t in self.top_tracks]
        track_list.set_tracks(formatted_tracks, show_album=True)

        # Update albums
        self._update_albums()

    def _update_albums(self) -> None:
        """Update albums table."""
        table = self.query_one("#artist-albums", DataTable)
        table.clear()

        for album in self.albums:
            album_id = album.get("id", "")
            release_date = album.get("release_date", "")[:4]
            album_type = album.get("album_type", "album").capitalize()
            total_tracks = album.get("total_tracks", 0)

            table.add_row(
                truncate_text(album.get("name", ""), 38),
                release_date,
                album_type,
                str(total_tracks),
                key=album_id,
            )

    def on_track_list_track_selected(self, event: TrackList.TrackSelected) -> None:
        """Handle track selection."""
        if hasattr(self.app, "play_uri"):
            self.app.play_uri(event.track_uri)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle album selection."""
        if event.data_table.id == "artist-albums" and event.row_key:
            album_id = str(event.row_key.value)
            self.app.push_screen("album", {"album_id": album_id})

    def action_go_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()
