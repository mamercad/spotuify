"""Custom Textual widgets for Spotuify."""

from .now_playing import NowPlaying
from .player_controls import PlayerControls
from .sidebar import Sidebar
from .track_list import TrackList
from .search_bar import SearchBar
from .volume_bar import VolumeBar
from .progress_bar import PlaybackProgress
from .device_selector import DeviceSelector

__all__ = [
    "NowPlaying",
    "PlayerControls",
    "Sidebar",
    "TrackList",
    "SearchBar",
    "VolumeBar",
    "PlaybackProgress",
    "DeviceSelector",
]
