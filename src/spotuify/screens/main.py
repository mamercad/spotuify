"""Main screen of the application."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label, Footer, Header
from textual.containers import Vertical, Horizontal, Container
from textual.reactive import reactive

from ..widgets.sidebar import Sidebar
from ..widgets.now_playing import NowPlaying
from ..widgets.player_controls import PlayerControls
from ..widgets.progress_bar import PlaybackProgress
from ..widgets.volume_bar import VolumeBar
from ..widgets.track_list import TrackList


class MainScreen(Screen):
    """Main application screen with sidebar and content area."""

    DEFAULT_CSS = """
    MainScreen {
        layout: grid;
        grid-size: 1;
        grid-rows: 1fr auto;
    }

    MainScreen .main-container {
        layout: horizontal;
        height: 100%;
    }

    MainScreen .content-area {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    MainScreen .content-header {
        height: 3;
        padding: 0 1;
    }

    MainScreen .content-title {
        text-style: bold;
        color: $text;
    }

    MainScreen .content-body {
        height: 1fr;
    }

    MainScreen .player-bar {
        height: 9;
        dock: bottom;
        background: $surface;
        border-top: solid $primary-darken-2;
        padding: 0 1;
    }

    MainScreen .player-left {
        width: 30%;
    }

    MainScreen .player-center {
        width: 40%;
        align: center middle;
    }

    MainScreen .player-right {
        width: 30%;
        align: right middle;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("space", "toggle_play", "Play/Pause"),
        ("n", "next_track", "Next"),
        ("p", "previous_track", "Previous"),
        ("s", "focus_search", "Search"),
        ("?", "show_help", "Help"),
        ("/", "focus_search", "Search"),
        ("+", "volume_up", "Vol +"),
        ("-", "volume_down", "Vol -"),
        ("m", "toggle_mute", "Mute"),
        ("r", "cycle_repeat", "Repeat"),
        ("z", "toggle_shuffle", "Shuffle"),
        ("d", "show_devices", "Devices"),
        ("l", "show_library", "Library"),
        ("h", "go_home", "Home"),
    ]

    content_title: reactive[str] = reactive("Home")

    def compose(self) -> ComposeResult:
        """Compose the main screen layout."""
        yield Header(show_clock=True)

        with Container(classes="main-container"):
            yield Sidebar(id="sidebar")

            with Vertical(classes="content-area"):
                with Horizontal(classes="content-header"):
                    yield Label(self.content_title, id="content-title", classes="content-title")

                with Container(classes="content-body"):
                    yield TrackList(id="main-track-list")

        with Horizontal(classes="player-bar"):
            with Vertical(classes="player-left"):
                yield NowPlaying(id="now-playing")

            with Vertical(classes="player-center"):
                yield PlayerControls(id="player-controls")
                yield PlaybackProgress(id="playback-progress")

            with Vertical(classes="player-right"):
                yield VolumeBar(id="volume-bar")

        yield Footer()

    def watch_content_title(self, title: str) -> None:
        """Update the content title display."""
        try:
            label = self.query_one("#content-title", Label)
            label.update(title)
        except Exception:
            pass

    def action_toggle_play(self) -> None:
        """Toggle play/pause."""
        self.app.action_toggle_play()

    def action_next_track(self) -> None:
        """Skip to next track."""
        self.app.action_next_track()

    def action_previous_track(self) -> None:
        """Skip to previous track."""
        self.app.action_previous_track()

    def action_focus_search(self) -> None:
        """Focus the search screen."""
        self.app.push_screen("search")

    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")

    def action_volume_up(self) -> None:
        """Increase volume."""
        self.app.action_volume_up()

    def action_volume_down(self) -> None:
        """Decrease volume."""
        self.app.action_volume_down()

    def action_toggle_mute(self) -> None:
        """Toggle mute."""
        volume_bar = self.query_one("#volume-bar", VolumeBar)
        volume_bar.toggle_mute()

    def action_cycle_repeat(self) -> None:
        """Cycle repeat mode."""
        self.app.action_cycle_repeat()

    def action_toggle_shuffle(self) -> None:
        """Toggle shuffle."""
        self.app.action_toggle_shuffle()

    def action_show_devices(self) -> None:
        """Show devices screen."""
        self.app.push_screen("devices")

    def action_show_library(self) -> None:
        """Show library screen."""
        self.app.push_screen("library")

    def action_go_home(self) -> None:
        """Go to home view."""
        self.content_title = "Home"
        self.app.load_home_content()
