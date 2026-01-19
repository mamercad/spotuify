"""Search screen."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label, TabbedContent, TabPane, DataTable
from textual.containers import Vertical, Container
from textual.message import Message

from ..widgets.search_bar import SearchBar
from ..utils.formatting import format_duration, format_artist_names, truncate_text


class SearchScreen(Screen):
    """Search screen for finding tracks, albums, artists, and playlists."""

    DEFAULT_CSS = """
    SearchScreen {
        layout: vertical;
    }

    SearchScreen .search-header {
        height: auto;
        padding: 1;
    }

    SearchScreen .search-results {
        height: 1fr;
        padding: 0 1;
    }

    SearchScreen TabbedContent {
        height: 100%;
    }

    SearchScreen TabPane {
        padding: 1;
    }

    SearchScreen DataTable {
        height: 100%;
    }

    SearchScreen .no-results {
        width: 100%;
        height: 100%;
        content-align: center middle;
        color: $text-muted;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("/", "focus_search", "Search"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.search_results: dict[str, Any] = {}

    def compose(self) -> ComposeResult:
        """Compose the search screen."""
        with Vertical(classes="search-header"):
            yield SearchBar(id="search-bar")

        with Container(classes="search-results"):
            with TabbedContent():
                with TabPane("Tracks", id="tracks-tab"):
                    yield DataTable(id="tracks-results", cursor_type="row")
                with TabPane("Albums", id="albums-tab"):
                    yield DataTable(id="albums-results", cursor_type="row")
                with TabPane("Artists", id="artists-tab"):
                    yield DataTable(id="artists-results", cursor_type="row")
                with TabPane("Playlists", id="playlists-tab"):
                    yield DataTable(id="playlists-results", cursor_type="row")

    def on_mount(self) -> None:
        """Initialize the results tables."""
        # Tracks table
        tracks = self.query_one("#tracks-results", DataTable)
        tracks.add_column("#", width=4, key="num")
        tracks.add_column("Title", width=35, key="title")
        tracks.add_column("Artist", width=25, key="artist")
        tracks.add_column("Album", width=25, key="album")
        tracks.add_column("Duration", width=8, key="duration")

        # Albums table
        albums = self.query_one("#albums-results", DataTable)
        albums.add_column("Album", width=40, key="name")
        albums.add_column("Artist", width=30, key="artist")
        albums.add_column("Year", width=6, key="year")
        albums.add_column("Tracks", width=8, key="tracks")

        # Artists table
        artists = self.query_one("#artists-results", DataTable)
        artists.add_column("Artist", width=40, key="name")
        artists.add_column("Followers", width=15, key="followers")
        artists.add_column("Genres", width=40, key="genres")

        # Playlists table
        playlists = self.query_one("#playlists-results", DataTable)
        playlists.add_column("Playlist", width=40, key="name")
        playlists.add_column("Owner", width=25, key="owner")
        playlists.add_column("Tracks", width=10, key="tracks")

        # Focus search bar
        self.query_one("#search-bar", SearchBar).focus_search()

    def on_search_bar_search_submitted(self, event: SearchBar.SearchSubmitted) -> None:
        """Handle search submission."""
        self.run_search(event.query)

    def run_search(self, query: str) -> None:
        """Execute search and update results."""
        if hasattr(self.app, "spotify") and self.app.spotify:
            results = self.app.spotify.search(query)
            self.search_results = results
            self._update_results()

    def _update_results(self) -> None:
        """Update all result tables."""
        self._update_tracks()
        self._update_albums()
        self._update_artists()
        self._update_playlists()

    def _update_tracks(self) -> None:
        """Update tracks results."""
        table = self.query_one("#tracks-results", DataTable)
        table.clear()

        tracks = self.search_results.get("tracks", {}).get("items", [])
        for i, track in enumerate(tracks, 1):
            track_id = track.get("id", "")
            table.add_row(
                str(i),
                truncate_text(track.get("name", ""), 33),
                truncate_text(format_artist_names(track.get("artists", [])), 23),
                truncate_text(track.get("album", {}).get("name", ""), 23),
                format_duration(track.get("duration_ms")),
                key=track_id,
            )

    def _update_albums(self) -> None:
        """Update albums results."""
        table = self.query_one("#albums-results", DataTable)
        table.clear()

        albums = self.search_results.get("albums", {}).get("items", [])
        for album in albums:
            album_id = album.get("id", "")
            release_date = album.get("release_date", "")[:4]
            table.add_row(
                truncate_text(album.get("name", ""), 38),
                truncate_text(format_artist_names(album.get("artists", [])), 28),
                release_date,
                str(album.get("total_tracks", 0)),
                key=album_id,
            )

    def _update_artists(self) -> None:
        """Update artists results."""
        table = self.query_one("#artists-results", DataTable)
        table.clear()

        artists = self.search_results.get("artists", {}).get("items", [])
        for artist in artists:
            artist_id = artist.get("id", "")
            followers = artist.get("followers", {}).get("total", 0)
            followers_str = f"{followers:,}" if followers else "0"
            genres = ", ".join(artist.get("genres", [])[:3])
            table.add_row(
                truncate_text(artist.get("name", ""), 38),
                followers_str,
                truncate_text(genres, 38),
                key=artist_id,
            )

    def _update_playlists(self) -> None:
        """Update playlists results."""
        table = self.query_one("#playlists-results", DataTable)
        table.clear()

        playlists = self.search_results.get("playlists", {}).get("items", [])
        for playlist in playlists:
            if not playlist:
                continue
            playlist_id = playlist.get("id", "")
            owner = playlist.get("owner", {}).get("display_name", "")
            tracks_count = playlist.get("tracks", {}).get("total", 0)
            table.add_row(
                truncate_text(playlist.get("name", ""), 38),
                truncate_text(owner, 23),
                str(tracks_count),
                key=playlist_id,
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in results."""
        table_id = event.data_table.id
        row_key = str(event.row_key.value) if event.row_key else ""

        if not row_key:
            return

        if table_id == "tracks-results":
            # Find the track and play it
            tracks = self.search_results.get("tracks", {}).get("items", [])
            for track in tracks:
                if track.get("id") == row_key:
                    uri = track.get("uri", f"spotify:track:{row_key}")
                    if hasattr(self.app, "play_uri"):
                        self.app.play_uri(uri)
                    break
        elif table_id == "albums-results":
            self.app.push_screen("album", {"album_id": row_key})
        elif table_id == "artists-results":
            self.app.push_screen("artist", {"artist_id": row_key})
        elif table_id == "playlists-results":
            self.app.push_screen("playlist", {"playlist_id": row_key})

    def action_go_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()

    def action_focus_search(self) -> None:
        """Focus the search input."""
        self.query_one("#search-bar", SearchBar).focus_search()
