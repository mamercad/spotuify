"""Player control buttons widget."""

from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message


class PlayerControls(Static):
    """Widget with playback control buttons."""

    DEFAULT_CSS = """
    PlayerControls {
        height: 3;
        align: center middle;
    }

    PlayerControls Horizontal {
        align: center middle;
        height: auto;
        width: auto;
    }

    PlayerControls Button {
        min-width: 5;
        margin: 0 1;
    }

    PlayerControls .control-btn {
        background: $surface;
        border: none;
    }

    PlayerControls .control-btn:hover {
        background: $surface-lighten-1;
    }

    PlayerControls .play-btn {
        min-width: 7;
        background: $success;
        color: $text;
    }

    PlayerControls .play-btn:hover {
        background: $success-lighten-1;
    }

    PlayerControls .shuffle-active {
        color: $success;
    }

    PlayerControls .repeat-active {
        color: $success;
    }
    """

    is_playing: reactive[bool] = reactive(False)
    shuffle_state: reactive[bool] = reactive(False)
    repeat_state: reactive[str] = reactive("off")  # off, context, track

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        with Horizontal():
            yield Button("🔀", id="shuffle-btn", classes="control-btn", variant="default")
            yield Button("⏮", id="prev-btn", classes="control-btn", variant="default")
            yield Button("▶", id="play-btn", classes="play-btn", variant="success")
            yield Button("⏭", id="next-btn", classes="control-btn", variant="default")
            yield Button("🔁", id="repeat-btn", classes="control-btn", variant="default")

    def update_state(
        self, is_playing: bool, shuffle_state: bool = False, repeat_state: str = "off"
    ) -> None:
        """Update the control states."""
        self.is_playing = is_playing
        self.shuffle_state = shuffle_state
        self.repeat_state = repeat_state
        self._update_display()

    def _update_display(self) -> None:
        """Update button displays."""
        # Update play/pause button
        play_btn = self.query_one("#play-btn", Button)
        play_btn.label = "⏸" if self.is_playing else "▶"

        # Update shuffle button
        shuffle_btn = self.query_one("#shuffle-btn", Button)
        if self.shuffle_state:
            shuffle_btn.add_class("shuffle-active")
        else:
            shuffle_btn.remove_class("shuffle-active")

        # Update repeat button
        repeat_btn = self.query_one("#repeat-btn", Button)
        if self.repeat_state == "off":
            repeat_btn.label = "🔁"
            repeat_btn.remove_class("repeat-active")
        elif self.repeat_state == "context":
            repeat_btn.label = "🔁"
            repeat_btn.add_class("repeat-active")
        elif self.repeat_state == "track":
            repeat_btn.label = "🔂"
            repeat_btn.add_class("repeat-active")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "play-btn":
            self.post_message(self.PlayPause())
        elif button_id == "prev-btn":
            self.post_message(self.Previous())
        elif button_id == "next-btn":
            self.post_message(self.Next())
        elif button_id == "shuffle-btn":
            self.post_message(self.ToggleShuffle())
        elif button_id == "repeat-btn":
            self.post_message(self.CycleRepeat())

    class PlayPause(Message):
        """Message posted when play/pause is pressed."""

        pass

    class Previous(Message):
        """Message posted when previous is pressed."""

        pass

    class Next(Message):
        """Message posted when next is pressed."""

        pass

    class ToggleShuffle(Message):
        """Message posted when shuffle is toggled."""

        pass

    class CycleRepeat(Message):
        """Message posted when repeat mode is cycled."""

        pass
