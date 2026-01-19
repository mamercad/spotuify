"""Main Spotuify application."""

from typing import Any
from textual.app import App
from textual.binding import Binding
from textual.css.query import NoMatches

from .api.client import SpotifyClient
from .utils.config import Config
from .screens.main import MainScreen
from .screens.search import SearchScreen
from .screens.playlist import PlaylistScreen
from .screens.album import AlbumScreen
from .screens.artist import ArtistScreen
from .screens.library import LibraryScreen
from .screens.devices import DevicesScreen
from .screens.help import HelpScreen
from .widgets.now_playing import NowPlaying
from .widgets.player_controls import PlayerControls
from .widgets.progress_bar import PlaybackProgress
from .widgets.volume_bar import VolumeBar
from .widgets.sidebar import Sidebar
from .widgets.track_list import TrackList


class SpotuifyApp(App):
    """The main Spotuify TUI application."""

    TITLE = "Spotuify"
    SUB_TITLE = "A Terminal Spotify Player"

    CSS = """
    Screen {
        background: $background;
    }
    
    /* Spotify-inspired color scheme */
    $primary: #1DB954;
    $primary-darken-1: #1aa34a;
    $primary-darken-2: #178f41;
    $primary-lighten-1: #1ed760;
    
    $background: #121212;
    $surface: #181818;
    $surface-lighten-1: #282828;
    $surface-lighten-2: #333333;
    
    $text: #FFFFFF;
    $text-muted: #B3B3B3;
    $text-disabled: #535353;
    
    $success: #1DB954;
    $success-lighten-1: #1ed760;
    $warning: #FFA500;
    $error: #E91429;
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True, priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
    ]

    SCREENS = {
        "main": MainScreen,
        "search": SearchScreen,
        "library": LibraryScreen,
        "devices": DevicesScreen,
        "help": HelpScreen,
    }

    def __init__(self) -> None:
        super().__init__()
        self.config = Config()
        self.spotify: SpotifyClient | None = None
        self._update_timer: Any = None
        self._current_device_id: str | None = None

    async def on_mount(self) -> None:
        """Handle app mount - authenticate and start."""
        # Try to authenticate
        self.spotify = SpotifyClient(self.config)

        if not self.config.is_configured():
            self.notify(
                "Please configure Spotify credentials in config file",
                severity="warning",
                timeout=10,
            )
            self.notify(
                f"Config location: {self.config.config_file}",
                timeout=10,
            )
        elif self.spotify.authenticate():
            self.notify("Connected to Spotify", severity="information")
            # Load initial data
            await self._load_initial_data()
            # Start playback state update timer
            self._update_timer = self.set_interval(1.0, self._update_playback_state)
        else:
            self.notify(
                "Failed to authenticate with Spotify. Please check your credentials.",
                severity="error",
            )

        # Push the main screen
        await self.push_screen("main")

    async def _load_initial_data(self) -> None:
        """Load initial data like playlists."""
        if not self.spotify:
            return

        try:
            # Load user playlists for sidebar
            playlists = self.spotify.get_user_playlists()
            playlist_items = playlists.get("items", [])

            # Update sidebar with playlists (when main screen is loaded)
            self.call_later(self._update_sidebar_playlists, playlist_items)
        except Exception as e:
            self.log.error(f"Failed to load initial data: {e}")

    def _update_sidebar_playlists(self, playlists: list[dict[str, Any]]) -> None:
        """Update sidebar with playlists."""
        try:
            sidebar = self.query_one(Sidebar)
            sidebar.set_playlists(playlists)
        except NoMatches:
            pass

    async def _update_playback_state(self) -> None:
        """Update the UI with current playback state."""
        if not self.spotify:
            return

        try:
            state = self.spotify.get_playback_state()
            if not state:
                return

            # Update now playing widget
            try:
                now_playing = self.query_one(NowPlaying)
                now_playing.update_track(
                    track=state.track,
                    is_playing=state.is_playing,
                    progress_ms=state.progress_ms,
                )
            except NoMatches:
                pass

            # Update player controls
            try:
                controls = self.query_one(PlayerControls)
                controls.update_state(
                    is_playing=state.is_playing,
                    shuffle_state=state.shuffle_state,
                    repeat_state=state.repeat_state,
                )
            except NoMatches:
                pass

            # Update progress bar
            try:
                progress = self.query_one(PlaybackProgress)
                progress.update_progress(state.progress_ms, state.duration_ms)
            except NoMatches:
                pass

            # Update volume bar
            try:
                volume = self.query_one(VolumeBar)
                volume.set_volume(state.volume_percent)
            except NoMatches:
                pass

            # Update track list current track indicator
            try:
                track_list = self.query_one(TrackList)
                track_id = state.track.get("id") if state.track else None
                track_list.set_current_track(track_id)
            except NoMatches:
                pass

            # Store current device
            if state.device:
                self._current_device_id = state.device.get("id")

        except Exception as e:
            self.log.error(f"Failed to update playback state: {e}")

    # ========================
    # Playback Actions
    # ========================

    def action_toggle_play(self) -> None:
        """Toggle play/pause."""
        if self.spotify:
            self.spotify.toggle_playback(self._current_device_id)

    def action_next_track(self) -> None:
        """Skip to next track."""
        if self.spotify:
            self.spotify.next_track(self._current_device_id)

    def action_previous_track(self) -> None:
        """Skip to previous track."""
        if self.spotify:
            self.spotify.previous_track(self._current_device_id)

    def action_volume_up(self) -> None:
        """Increase volume."""
        if self.spotify:
            state = self.spotify.get_playback_state()
            if state:
                new_volume = min(100, state.volume_percent + 5)
                self.spotify.set_volume(new_volume, self._current_device_id)

    def action_volume_down(self) -> None:
        """Decrease volume."""
        if self.spotify:
            state = self.spotify.get_playback_state()
            if state:
                new_volume = max(0, state.volume_percent - 5)
                self.spotify.set_volume(new_volume, self._current_device_id)

    def action_toggle_shuffle(self) -> None:
        """Toggle shuffle mode."""
        if self.spotify:
            self.spotify.toggle_shuffle(self._current_device_id)

    def action_cycle_repeat(self) -> None:
        """Cycle repeat mode."""
        if self.spotify:
            self.spotify.cycle_repeat(self._current_device_id)

    def play_uri(self, uri: str, context_uri: str | None = None, offset: int | None = None) -> None:
        """Play a Spotify URI."""
        if self.spotify:
            self.spotify.play_uri(
                uri,
                device_id=self._current_device_id,
                context_uri=context_uri,
                offset=offset,
            )

    def load_home_content(self) -> None:
        """Load home screen content (recently played)."""
        if not self.spotify:
            return

        try:
            recent = self.spotify.get_recently_played(limit=50)
            items = recent.get("items", [])

            # Format for TrackList
            tracks = [{"track": item.get("track")} for item in items if item.get("track")]

            try:
                track_list = self.query_one("#main-track-list", TrackList)
                track_list.set_tracks(tracks, show_added_at=False)
            except NoMatches:
                pass
        except Exception as e:
            self.log.error(f"Failed to load home content: {e}")

    # ========================
    # Screen Push with Data
    # ========================

    def push_screen(
        self,
        screen: str,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Push a screen, optionally with data."""
        if screen == "playlist" and data and "playlist_id" in data:
            return super().push_screen(PlaylistScreen(playlist_id=data["playlist_id"]))
        elif screen == "album" and data and "album_id" in data:
            return super().push_screen(AlbumScreen(album_id=data["album_id"]))
        elif screen == "artist" and data and "artist_id" in data:
            return super().push_screen(ArtistScreen(artist_id=data["artist_id"]))
        else:
            return super().push_screen(screen, **kwargs)

    # ========================
    # Message Handlers
    # ========================

    def on_player_controls_play_pause(self, event: PlayerControls.PlayPause) -> None:
        """Handle play/pause from controls."""
        self.action_toggle_play()

    def on_player_controls_previous(self, event: PlayerControls.Previous) -> None:
        """Handle previous from controls."""
        self.action_previous_track()

    def on_player_controls_next(self, event: PlayerControls.Next) -> None:
        """Handle next from controls."""
        self.action_next_track()

    def on_player_controls_toggle_shuffle(self, event: PlayerControls.ToggleShuffle) -> None:
        """Handle shuffle toggle from controls."""
        self.action_toggle_shuffle()

    def on_player_controls_cycle_repeat(self, event: PlayerControls.CycleRepeat) -> None:
        """Handle repeat cycle from controls."""
        self.action_cycle_repeat()

    def on_volume_bar_volume_changed(self, event: VolumeBar.VolumeChanged) -> None:
        """Handle volume change from volume bar."""
        if self.spotify:
            self.spotify.set_volume(event.volume, self._current_device_id)

    def on_playback_progress_seek(self, event: PlaybackProgress.Seek) -> None:
        """Handle seek from progress bar."""
        if self.spotify:
            self.spotify.seek(event.position_ms, self._current_device_id)

    def on_sidebar_item_selected(self, event: Sidebar.ItemSelected) -> None:
        """Handle sidebar item selection."""
        if event.item_type == "nav":
            if event.item_id == "home":
                self.load_home_content()
            elif event.item_id == "search":
                self.push_screen("search")
            elif event.item_id == "library":
                self.push_screen("library")
            elif event.item_id == "recent":
                self.load_home_content()
            elif event.item_id == "devices":
                self.push_screen("devices")
        elif event.item_type == "library":
            if event.item_id in ("liked", "albums", "artists"):
                self.push_screen("library")
        elif event.item_type == "playlist":
            self.push_screen("playlist", {"playlist_id": event.item_id})

    def on_track_list_track_selected(self, event: TrackList.TrackSelected) -> None:
        """Handle track selection from main track list."""
        self.play_uri(
            event.track_uri,
            context_uri=event.context_uri,
            offset=event.index,
        )
