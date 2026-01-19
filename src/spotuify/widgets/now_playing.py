"""Now Playing widget showing current track information."""

from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

from ..utils.formatting import format_duration, format_artist_names, truncate_text


class NowPlaying(Static):
    """Widget displaying currently playing track information."""

    DEFAULT_CSS = """
    NowPlaying {
        height: auto;
        min-height: 7;
        padding: 0 1;
        background: $surface;
        border: solid $primary;
    }

    NowPlaying .track-info {
        height: auto;
    }

    NowPlaying .track-title {
        text-style: bold;
        color: $text;
    }

    NowPlaying .track-artist {
        color: $text-muted;
    }

    NowPlaying .track-album {
        color: $text-disabled;
        text-style: italic;
    }

    NowPlaying .playing-indicator {
        color: $success;
    }

    NowPlaying .paused-indicator {
        color: $warning;
    }
    """

    # Reactive attributes
    track_name: reactive[str] = reactive("No track playing")
    artist_name: reactive[str] = reactive("")
    album_name: reactive[str] = reactive("")
    is_playing: reactive[bool] = reactive(False)
    duration_ms: reactive[int] = reactive(0)
    progress_ms: reactive[int] = reactive(0)
    album_art_url: reactive[str | None] = reactive(None)

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        with Vertical(classes="track-info"):
            yield Label("", id="status-indicator")
            yield Label("No track playing", id="track-title", classes="track-title")
            yield Label("", id="track-artist", classes="track-artist")
            yield Label("", id="track-album", classes="track-album")

    def update_track(
        self,
        track: dict | None = None,
        is_playing: bool = False,
        progress_ms: int = 0,
    ) -> None:
        """Update the displayed track information."""
        self.is_playing = is_playing
        self.progress_ms = progress_ms

        if track:
            self.track_name = track.get("name", "Unknown Track")
            artists = track.get("artists", [])
            self.artist_name = format_artist_names(artists)
            album = track.get("album", {})
            self.album_name = album.get("name", "")
            self.duration_ms = track.get("duration_ms", 0)

            # Get album art URL
            images = album.get("images", [])
            self.album_art_url = images[0].get("url") if images else None
        else:
            self.track_name = "No track playing"
            self.artist_name = ""
            self.album_name = ""
            self.duration_ms = 0
            self.album_art_url = None

        self._update_display()

    def _update_display(self) -> None:
        """Update the display labels."""
        # Update status indicator
        indicator = self.query_one("#status-indicator", Label)
        if self.track_name != "No track playing":
            if self.is_playing:
                indicator.update(Text("▶ Now Playing", style="bold green"))
            else:
                indicator.update(Text("⏸ Paused", style="bold yellow"))
        else:
            indicator.update("")

        # Update track info
        title = self.query_one("#track-title", Label)
        title.update(truncate_text(self.track_name, 50))

        artist = self.query_one("#track-artist", Label)
        artist.update(truncate_text(self.artist_name, 50) if self.artist_name else "")

        album = self.query_one("#track-album", Label)
        album.update(truncate_text(self.album_name, 50) if self.album_name else "")

    def watch_is_playing(self, playing: bool) -> None:
        """React to playing state changes."""
        self._update_display()
