"""Library screen."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label, TabbedContent, TabPane, DataTable
from textual.containers import Vertical
from textual.reactive import reactive

from ..widgets.track_list import TrackList
from ..utils.formatting import format_artist_names, truncate_text


class LibraryScreen(Screen):
    """Screen for viewing user's library (saved tracks, albums, artists)."""

    DEFAULT_CSS = """
    LibraryScreen {
        layout: vertical;
    }

    LibraryScreen .library-header {
        height: 3;
        padding: 1;
        background: $surface;
        border-bottom: solid $primary-darken-2;
    }

    LibraryScreen .library-title {
        text-style: bold;
    }

    LibraryScreen .library-content {
        height: 1fr;
        padding: 1;
    }

    LibraryScreen TabbedContent {
        height: 100%;
    }

    LibraryScreen TabPane {
        padding: 1;
    }

    LibraryScreen DataTable {
        height: 100%;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("r", "refresh", "Refresh"),
    ]

    saved_tracks: reactive[list[dict[str, Any]]] = reactive(list)
    saved_albums: reactive[list[dict[str, Any]]] = reactive(list)
    followed_artists: reactive[list[dict[str, Any]]] = reactive(list)

    def compose(self) -> ComposeResult:
        """Compose the library screen."""
        with Vertical(classes="library-header"):
            yield Label("Your Library", classes="library-title")

        with Vertical(classes="library-content"):
            with TabbedContent():
                with TabPane("Liked Songs", id="liked-tab"):
                    yield TrackList(id="liked-tracks")
                with TabPane("Albums", id="albums-tab"):
                    yield DataTable(id="saved-albums", cursor_type="row")
                with TabPane("Artists", id="artists-tab"):
                    yield DataTable(id="followed-artists", cursor_type="row")

    def on_mount(self) -> None:
        """Initialize tables and load data."""
        # Setup albums table
        albums_table = self.query_one("#saved-albums", DataTable)
        albums_table.add_column("Album", width=40, key="name")
        albums_table.add_column("Artist", width=30, key="artist")
        albums_table.add_column("Added", width=12, key="added")

        # Setup artists table
        artists_table = self.query_one("#followed-artists", DataTable)
        artists_table.add_column("Artist", width=40, key="name")
        artists_table.add_column("Followers", width=15, key="followers")
        artists_table.add_column("Genres", width=40, key="genres")

        self.load_library()

    def load_library(self) -> None:
        """Load library data."""
        if not hasattr(self.app, "spotify") or not self.app.spotify:
            return

        # Load saved tracks
        tracks_result = self.app.spotify.get_saved_tracks(limit=50)
        self.saved_tracks = tracks_result.get("items", [])

        # Load saved albums
        albums_result = self.app.spotify.get_saved_albums(limit=50)
        self.saved_albums = albums_result.get("items", [])

        # Load followed artists
        artists_result = self.app.spotify.get_followed_artists(limit=50)
        self.followed_artists = artists_result.get("artists", {}).get("items", [])

        self._update_display()

    def _update_display(self) -> None:
        """Update all displays."""
        self._update_tracks()
        self._update_albums()
        self._update_artists()

    def _update_tracks(self) -> None:
        """Update liked tracks display."""
        track_list = self.query_one("#liked-tracks", TrackList)
        track_list.set_tracks(
            self.saved_tracks,
            context_uri="spotify:user:library",  # Special URI for liked songs
            show_added_at=True,
        )

    def _update_albums(self) -> None:
        """Update saved albums display."""
        table = self.query_one("#saved-albums", DataTable)
        table.clear()

        for item in self.saved_albums:
            album = item.get("album", {})
            album_id = album.get("id", "")
            added_at = item.get("added_at", "")[:10]

            table.add_row(
                truncate_text(album.get("name", ""), 38),
                truncate_text(format_artist_names(album.get("artists", [])), 28),
                added_at,
                key=album_id,
            )

    def _update_artists(self) -> None:
        """Update followed artists display."""
        table = self.query_one("#followed-artists", DataTable)
        table.clear()

        for artist in self.followed_artists:
            artist_id = artist.get("id", "")
            followers = artist.get("followers", {}).get("total", 0)
            genres = ", ".join(artist.get("genres", [])[:3])

            table.add_row(
                truncate_text(artist.get("name", ""), 38),
                f"{followers:,}",
                truncate_text(genres, 38),
                key=artist_id,
            )

    def on_track_list_track_selected(self, event: TrackList.TrackSelected) -> None:
        """Handle track selection."""
        if hasattr(self.app, "play_uri"):
            # For liked songs, we can play from the context
            self.app.play_uri(event.track_uri)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle table row selection."""
        if not event.row_key:
            return

        item_id = str(event.row_key.value)
        table_id = event.data_table.id

        if table_id == "saved-albums":
            self.app.push_screen("album", {"album_id": item_id})
        elif table_id == "followed-artists":
            self.app.push_screen("artist", {"artist_id": item_id})

    def action_go_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()

    def action_refresh(self) -> None:
        """Refresh library data."""
        self.load_library()
