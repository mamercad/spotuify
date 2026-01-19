"""Devices screen."""

from typing import Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.containers import Vertical
from textual.reactive import reactive

from ..widgets.device_selector import DeviceSelector


class DevicesScreen(Screen):
    """Screen for selecting playback device."""

    DEFAULT_CSS = """
    DevicesScreen {
        layout: vertical;
        align: center middle;
    }

    DevicesScreen .devices-container {
        width: 60;
        height: auto;
        max-height: 80%;
        background: $surface;
        border: solid $primary;
        padding: 1 2;
    }

    DevicesScreen .devices-title {
        text-style: bold;
        text-align: center;
        padding: 1;
    }

    DevicesScreen .devices-hint {
        color: $text-muted;
        text-align: center;
        padding: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the devices screen."""
        with Vertical(classes="devices-container"):
            yield Label("Select Playback Device", classes="devices-title")
            yield DeviceSelector(id="device-selector")
            yield Label("Press 'r' to refresh devices", classes="devices-hint")

    def on_mount(self) -> None:
        """Load devices when mounted."""
        self.load_devices()

    def load_devices(self) -> None:
        """Load available devices."""
        if hasattr(self.app, "spotify") and self.app.spotify:
            devices = self.app.spotify.get_devices()
            selector = self.query_one("#device-selector", DeviceSelector)
            selector.set_devices(devices)

    def on_device_selector_device_selected(self, event: DeviceSelector.DeviceSelected) -> None:
        """Handle device selection."""
        if hasattr(self.app, "spotify") and self.app.spotify:
            success = self.app.spotify.transfer_playback(event.device_id)
            if success:
                self.notify(f"Switched to {event.device_name}")
                self.app.pop_screen()
            else:
                self.notify("Failed to switch device", severity="error")

    def action_go_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()

    def action_refresh(self) -> None:
        """Refresh devices list."""
        self.load_devices()
        self.notify("Devices refreshed")
