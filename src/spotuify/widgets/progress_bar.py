"""Playback progress bar widget."""

from textual.app import ComposeResult
from textual.widgets import Static, Label, ProgressBar
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message
from textual import events

from ..utils.formatting import format_duration


class PlaybackProgress(Static):
    """Widget displaying playback progress with seek capability."""

    DEFAULT_CSS = """
    PlaybackProgress {
        height: 3;
        padding: 0 1;
    }

    PlaybackProgress Horizontal {
        height: 1;
        align: center middle;
    }

    PlaybackProgress .time-label {
        width: 6;
        text-align: center;
    }

    PlaybackProgress .progress-container {
        height: 1;
        padding: 0 1;
    }

    PlaybackProgress ProgressBar {
        width: 1fr;
        padding: 0;
    }

    PlaybackProgress ProgressBar > .bar--bar {
        color: $success;
    }

    PlaybackProgress ProgressBar > .bar--complete {
        color: $success;
    }
    """

    progress_ms: reactive[int] = reactive(0)
    duration_ms: reactive[int] = reactive(0)
    can_seek: reactive[bool] = reactive(True)

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        with Horizontal(classes="progress-container"):
            yield Label("0:00", id="current-time", classes="time-label")
            yield ProgressBar(total=100, show_eta=False, show_percentage=False, id="progress")
            yield Label("0:00", id="total-time", classes="time-label")

    def update_progress(self, progress_ms: int, duration_ms: int) -> None:
        """Update the progress display."""
        self.progress_ms = progress_ms
        self.duration_ms = duration_ms
        self._update_display()

    def _update_display(self) -> None:
        """Update the visual display."""
        # Update time labels
        current = self.query_one("#current-time", Label)
        current.update(format_duration(self.progress_ms))

        total = self.query_one("#total-time", Label)
        total.update(format_duration(self.duration_ms))

        # Update progress bar
        progress_bar = self.query_one("#progress", ProgressBar)
        if self.duration_ms > 0:
            percentage = (self.progress_ms / self.duration_ms) * 100
            progress_bar.update(progress=percentage)
        else:
            progress_bar.update(progress=0)

    def on_click(self, event: events.Click) -> None:
        """Handle click to seek."""
        if not self.can_seek or self.duration_ms == 0:
            return

        # Find the progress bar and calculate seek position
        progress_bar = self.query_one("#progress", ProgressBar)

        # Get the click position relative to the progress bar
        # This is a simplified version - actual implementation would need
        # to calculate based on the progress bar's actual position
        bar_region = progress_bar.region
        if bar_region.x <= event.x <= bar_region.x + bar_region.width:
            relative_x = event.x - bar_region.x
            percentage = relative_x / bar_region.width
            seek_position = int(percentage * self.duration_ms)

            # Post a seek event
            self.post_message(self.Seek(seek_position))

    class Seek(Message):
        """Message posted when user seeks to a position."""

        def __init__(self, position_ms: int) -> None:
            self.position_ms = position_ms
            super().__init__()
