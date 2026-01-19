"""Help screen showing keyboard shortcuts."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label, DataTable
from textual.containers import Vertical, Center


class HelpScreen(Screen):
    """Screen displaying keyboard shortcuts and help."""

    DEFAULT_CSS = """
    HelpScreen {
        layout: vertical;
        align: center middle;
    }

    HelpScreen .help-container {
        width: 70;
        height: auto;
        max-height: 90%;
        background: $surface;
        border: solid $primary;
        padding: 1 2;
    }

    HelpScreen .help-title {
        text-style: bold;
        text-align: center;
        padding: 1;
        color: $primary;
    }

    HelpScreen .section-title {
        text-style: bold;
        padding: 1 0 0 0;
        color: $text;
    }

    HelpScreen DataTable {
        height: auto;
        max-height: 40;
    }

    HelpScreen .help-footer {
        text-align: center;
        color: $text-muted;
        padding: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("q", "go_back", "Close"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the help screen."""
        with Vertical(classes="help-container"):
            yield Label("Spotuify - Keyboard Shortcuts", classes="help-title")

            yield Label("Playback Controls", classes="section-title")
            yield DataTable(id="playback-shortcuts", show_header=False)

            yield Label("Navigation", classes="section-title")
            yield DataTable(id="navigation-shortcuts", show_header=False)

            yield Label("Volume", classes="section-title")
            yield DataTable(id="volume-shortcuts", show_header=False)

            yield Label("Press Escape or 'q' to close", classes="help-footer")

    def on_mount(self) -> None:
        """Populate shortcut tables."""
        # Playback shortcuts
        playback = self.query_one("#playback-shortcuts", DataTable)
        playback.add_column("Key", width=15)
        playback.add_column("Action", width=40)
        playback_shortcuts = [
            ("Space", "Play / Pause"),
            ("n", "Next track"),
            ("p", "Previous track"),
            ("z", "Toggle shuffle"),
            ("r", "Cycle repeat mode (off → all → one)"),
        ]
        for key, action in playback_shortcuts:
            playback.add_row(key, action)

        # Navigation shortcuts
        navigation = self.query_one("#navigation-shortcuts", DataTable)
        navigation.add_column("Key", width=15)
        navigation.add_column("Action", width=40)
        nav_shortcuts = [
            ("h", "Go to Home"),
            ("s or /", "Open Search"),
            ("l", "Open Library"),
            ("d", "Select device"),
            ("?", "Show this help"),
            ("Escape", "Go back / Close modal"),
            ("q", "Quit application"),
        ]
        for key, action in nav_shortcuts:
            navigation.add_row(key, action)

        # Volume shortcuts
        volume = self.query_one("#volume-shortcuts", DataTable)
        volume.add_column("Key", width=15)
        volume.add_column("Action", width=40)
        volume_shortcuts = [
            ("+", "Increase volume"),
            ("-", "Decrease volume"),
            ("m", "Toggle mute"),
        ]
        for key, action in volume_shortcuts:
            volume.add_row(key, action)

    def action_go_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()
