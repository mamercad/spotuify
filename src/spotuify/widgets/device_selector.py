"""Device selector widget."""

from typing import Any
from textual.app import ComposeResult
from textual.widgets import Static, Label, ListView, ListItem
from textual.containers import Vertical
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text


class DeviceItem(ListItem):
    """A single device item in the list."""

    def __init__(
        self,
        device_id: str,
        name: str,
        device_type: str,
        is_active: bool = False,
        volume: int = 50,
    ) -> None:
        super().__init__()
        self.device_id = device_id
        self.device_name = name
        self.device_type = device_type
        self.is_active = is_active
        self.volume = volume

    def compose(self) -> ComposeResult:
        """Compose the device item."""
        # Get icon based on device type
        icons = {
            "Computer": "💻",
            "Smartphone": "📱",
            "Speaker": "🔊",
            "TV": "📺",
            "AVR": "🎛️",
            "STB": "📦",
            "AudioDongle": "🎵",
            "GameConsole": "🎮",
            "CastVideo": "📹",
            "CastAudio": "🔈",
            "Automobile": "🚗",
        }
        icon = icons.get(self.device_type, "🎵")

        status = "● " if self.is_active else "○ "
        text = Text()
        text.append(status, style="green" if self.is_active else "dim")
        text.append(f"{icon} {self.device_name}")

        yield Label(text)


class DeviceSelector(Static):
    """Widget for selecting playback device."""

    DEFAULT_CSS = """
    DeviceSelector {
        height: auto;
        width: 100%;
        padding: 1;
    }

    DeviceSelector .section-title {
        text-style: bold;
        padding: 0 0 1 0;
    }

    DeviceSelector ListView {
        height: auto;
        max-height: 15;
        background: $surface;
    }

    DeviceSelector ListItem {
        padding: 1;
    }

    DeviceSelector ListItem:hover {
        background: $surface-lighten-1;
    }

    DeviceSelector ListItem.-active {
        background: $primary-darken-1;
    }

    DeviceSelector .no-devices {
        color: $text-muted;
        padding: 1;
    }
    """

    devices: reactive[list[dict[str, Any]]] = reactive(list)
    active_device_id: reactive[str | None] = reactive(None)

    def compose(self) -> ComposeResult:
        """Compose the widget layout."""
        with Vertical():
            yield Label("Available Devices", classes="section-title")
            yield ListView(id="devices-list")
            yield Label("No devices found", id="no-devices", classes="no-devices")

    def on_mount(self) -> None:
        """Initialize the device list."""
        self._update_display()

    def set_devices(self, devices: list[dict[str, Any]]) -> None:
        """Set the available devices."""
        self.devices = devices

        # Find active device
        for device in devices:
            if device.get("is_active"):
                self.active_device_id = device.get("id")
                break

        self._update_display()

    def _update_display(self) -> None:
        """Update the devices display."""
        device_list = self.query_one("#devices-list", ListView)
        no_devices = self.query_one("#no-devices", Label)

        device_list.clear()

        if not self.devices:
            no_devices.display = True
            device_list.display = False
            return

        no_devices.display = False
        device_list.display = True

        for device in self.devices:
            item = DeviceItem(
                device_id=device.get("id", ""),
                name=device.get("name", "Unknown Device"),
                device_type=device.get("type", "Computer"),
                is_active=device.get("is_active", False),
                volume=device.get("volume_percent", 50),
            )
            device_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle device selection."""
        item = event.item
        if isinstance(item, DeviceItem):
            self.post_message(self.DeviceSelected(item.device_id, item.device_name))

    class DeviceSelected(Message):
        """Message posted when a device is selected."""

        def __init__(self, device_id: str, device_name: str) -> None:
            self.device_id = device_id
            self.device_name = device_name
            super().__init__()
