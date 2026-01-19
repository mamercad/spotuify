"""Track list widget for displaying lists of tracks."""

from typing import Any
from textual.app import ComposeResult
from textual.widgets import Static, Label, DataTable
from textual.containers import Vertical
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text

from ..utils.formatting import format_duration, format_artist_names, truncate_text


class TrackList(Static):
    """Widget displaying a list of tracks in a table format."""

    DEFAULT_CSS = """
    TrackList {
        height: 100%;
        width: 100%;
    }

    TrackList DataTable {
        height: 100%;
        width: 100%;
    }

    TrackList DataTable > .datatable--header {
        text-style: bold;
        background: $surface;
    }

    TrackList DataTable > .datatable--cursor {
        background: $primary-darken-1;
    }

    TrackList DataTable > .datatable--hover {
        background: $surface-lighten-1;
    }

    TrackList .empty-message {
        width: 100%;
        height: 100%;
        content-align: center middle;
        color: $text-muted;
    }
    """

    tracks: reactive[list[dict[str, Any]]] = reactive(list)
    context_uri: reactive[str | None] = reactive(None)
    show_album: reactive[bool] = reactive(True)
    show_added_at: reactive[bool] = reactive(False)
    current_track_id: reactive[str | None] = reactive(None)

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        yield DataTable(id="tracks-table", cursor_type="row")

    def on_mount(self) -> None:
        """Initialize the table."""
        table = self.query_one("#tracks-table", DataTable)
        table.add_column("#", width=4, key="num")
        table.add_column("Title", width=30, key="title")
        table.add_column("Artist", width=25, key="artist")
        if self.show_album:
            table.add_column("Album", width=25, key="album")
        table.add_column("Duration", width=8, key="duration")
        if self.show_added_at:
            table.add_column("Added", width=12, key="added")

    def set_tracks(
        self,
        tracks: list[dict[str, Any]],
        context_uri: str | None = None,
        show_album: bool = True,
        show_added_at: bool = False,
    ) -> None:
        """Set the tracks to display."""
        self.show_album = show_album
        self.show_added_at = show_added_at
        self.context_uri = context_uri
        self.tracks = tracks
        self._update_table()

    def _update_table(self) -> None:
        """Update the table with current tracks."""
        table = self.query_one("#tracks-table", DataTable)
        table.clear()

        for i, track_item in enumerate(self.tracks, 1):
            # Handle both playlist tracks (with 'track' key) and direct tracks
            track = track_item.get("track") if "track" in track_item else track_item

            if not track:
                continue

            track_id = track.get("id", "")
            name = track.get("name", "Unknown")
            artists = format_artist_names(track.get("artists", []))
            album = track.get("album", {}).get("name", "") if self.show_album else ""
            duration = format_duration(track.get("duration_ms"))

            # Check if this is the currently playing track
            is_current = track_id == self.current_track_id

            # Create styled text for currently playing track
            num_text = Text(f"▶ " if is_current else f"{i}")
            if is_current:
                num_text.stylize("bold green")

            title_text = Text(truncate_text(name, 28))
            if is_current:
                title_text.stylize("bold green")

            row_data = [
                num_text,
                title_text,
                truncate_text(artists, 23),
            ]

            if self.show_album:
                row_data.append(truncate_text(album, 23))

            row_data.append(duration)

            if self.show_added_at:
                added_at = track_item.get("added_at", "")[:10] if "added_at" in track_item else ""
                row_data.append(added_at)

            table.add_row(*row_data, key=track_id)

    def set_current_track(self, track_id: str | None) -> None:
        """Set the currently playing track."""
        self.current_track_id = track_id
        self._update_table()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection (Enter key)."""
        if event.row_key:
            track_id = str(event.row_key.value)
            # Find the track data
            for i, track_item in enumerate(self.tracks):
                track = track_item.get("track") if "track" in track_item else track_item
                if track and track.get("id") == track_id:
                    uri = track.get("uri", f"spotify:track:{track_id}")
                    self.post_message(
                        self.TrackSelected(
                            track_id=track_id,
                            track_uri=uri,
                            track_data=track,
                            index=i,
                            context_uri=self.context_uri,
                        )
                    )
                    break

    class TrackSelected(Message):
        """Message posted when a track is selected."""

        def __init__(
            self,
            track_id: str,
            track_uri: str,
            track_data: dict[str, Any],
            index: int,
            context_uri: str | None = None,
        ) -> None:
            self.track_id = track_id
            self.track_uri = track_uri
            self.track_data = track_data
            self.index = index
            self.context_uri = context_uri
            super().__init__()
