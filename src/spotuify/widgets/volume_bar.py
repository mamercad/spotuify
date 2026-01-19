"""Volume control widget."""

from textual.app import ComposeResult
from textual.widgets import Static, Label, ProgressBar, Button
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message
from textual import events
from rich.text import Text


class VolumeBar(Static):
    """Widget for controlling playback volume."""

    DEFAULT_CSS = """
    VolumeBar {
        height: 1;
        width: 100%;
        layout: horizontal;
    }

    VolumeBar .volume-icon {
        width: 3;
        text-align: center;
    }

    VolumeBar ProgressBar {
        width: 15;
        padding: 0;
    }

    VolumeBar ProgressBar > .bar--bar {
        color: $primary;
    }

    VolumeBar .volume-percent {
        width: 4;
        text-align: right;
        margin-left: 1;
    }
    """

    volume: reactive[int] = reactive(50)
    is_muted: reactive[bool] = reactive(False)
    _pre_mute_volume: int = 50

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        with Horizontal():
            yield Label("🔊", id="volume-icon", classes="volume-icon")
            yield ProgressBar(total=100, show_eta=False, show_percentage=False, id="volume-bar")
            yield Label("50%", id="volume-percent", classes="volume-percent")

    def on_mount(self) -> None:
        """Initialize volume display."""
        self._update_display()

    def set_volume(self, volume: int) -> None:
        """Set the volume level (0-100)."""
        self.volume = max(0, min(100, volume))
        if self.volume > 0:
            self.is_muted = False
        self._update_display()

    def _update_display(self) -> None:
        """Update the volume display."""
        # Update icon based on volume level
        icon = self.query_one("#volume-icon", Label)
        if self.is_muted or self.volume == 0:
            icon.update("🔇")
        elif self.volume < 30:
            icon.update("🔈")
        elif self.volume < 70:
            icon.update("🔉")
        else:
            icon.update("🔊")

        # Update progress bar
        bar = self.query_one("#volume-bar", ProgressBar)
        bar.update(progress=self.volume if not self.is_muted else 0)

        # Update percentage
        percent = self.query_one("#volume-percent", Label)
        percent.update(f"{self.volume}%")

    def toggle_mute(self) -> None:
        """Toggle mute state."""
        if self.is_muted:
            self.is_muted = False
            self.post_message(self.VolumeChanged(self.volume))
        else:
            self._pre_mute_volume = self.volume
            self.is_muted = True
            self.post_message(self.VolumeChanged(0))
        self._update_display()

    def increase_volume(self, amount: int = 5) -> None:
        """Increase volume by amount."""
        self.set_volume(self.volume + amount)
        self.post_message(self.VolumeChanged(self.volume))

    def decrease_volume(self, amount: int = 5) -> None:
        """Decrease volume by amount."""
        self.set_volume(self.volume - amount)
        self.post_message(self.VolumeChanged(self.volume))

    def on_click(self, event: events.Click) -> None:
        """Handle click on volume bar to set volume."""
        bar = self.query_one("#volume-bar", ProgressBar)
        bar_region = bar.region

        if bar_region.x <= event.x <= bar_region.x + bar_region.width:
            relative_x = event.x - bar_region.x
            percentage = int((relative_x / bar_region.width) * 100)
            self.set_volume(percentage)
            self.post_message(self.VolumeChanged(self.volume))

    class VolumeChanged(Message):
        """Message posted when volume changes."""

        def __init__(self, volume: int) -> None:
            self.volume = volume
            super().__init__()
