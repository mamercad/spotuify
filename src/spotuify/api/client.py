"""Spotify API client wrapper."""

from typing import Any
from dataclasses import dataclass

import spotipy

from .auth import SpotifyAuth
from ..utils.config import Config


@dataclass
class PlaybackState:
    """Current playback state."""

    is_playing: bool = False
    track: dict[str, Any] | None = None
    device: dict[str, Any] | None = None
    progress_ms: int = 0
    duration_ms: int = 0
    shuffle_state: bool = False
    repeat_state: str = "off"  # off, track, context
    volume_percent: int = 50
    context: dict[str, Any] | None = None


class SpotifyClient:
    """High-level Spotify API client for Spotuify."""

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()
        self.auth = SpotifyAuth(self.config)
        self._sp: spotipy.Spotify | None = None

    @property
    def sp(self) -> spotipy.Spotify:
        """Get the underlying Spotipy client."""
        if self._sp is None:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._sp

    def is_authenticated(self) -> bool:
        """Check if client is authenticated."""
        return self._sp is not None

    def authenticate(self) -> bool:
        """Authenticate with Spotify."""
        token_info = self.auth.get_cached_token()
        if token_info:
            self._sp = spotipy.Spotify(auth=token_info["access_token"])
            return True
        return False

    def _ensure_authenticated(self) -> None:
        """Ensure client is authenticated, raise if not."""
        if not self.is_authenticated():
            raise RuntimeError("Not authenticated")

    # ========================
    # Playback Control
    # ========================

    def get_playback_state(self) -> PlaybackState | None:
        """Get current playback state."""
        self._ensure_authenticated()
        try:
            current = self.sp.current_playback()
            if not current:
                return PlaybackState()

            return PlaybackState(
                is_playing=current.get("is_playing", False),
                track=current.get("item"),
                device=current.get("device"),
                progress_ms=current.get("progress_ms", 0) or 0,
                duration_ms=current.get("item", {}).get("duration_ms", 0)
                if current.get("item")
                else 0,
                shuffle_state=current.get("shuffle_state", False),
                repeat_state=current.get("repeat_state", "off"),
                volume_percent=current.get("device", {}).get("volume_percent", 50)
                if current.get("device")
                else 50,
                context=current.get("context"),
            )
        except spotipy.SpotifyException:
            return None

    def play(self, device_id: str | None = None) -> bool:
        """Resume playback."""
        self._ensure_authenticated()
        try:
            self.sp.start_playback(device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def pause(self, device_id: str | None = None) -> bool:
        """Pause playback."""
        self._ensure_authenticated()
        try:
            self.sp.pause_playback(device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def toggle_playback(self, device_id: str | None = None) -> bool:
        """Toggle play/pause."""
        state = self.get_playback_state()
        if state and state.is_playing:
            return self.pause(device_id)
        return self.play(device_id)

    def next_track(self, device_id: str | None = None) -> bool:
        """Skip to next track."""
        self._ensure_authenticated()
        try:
            self.sp.next_track(device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def previous_track(self, device_id: str | None = None) -> bool:
        """Skip to previous track."""
        self._ensure_authenticated()
        try:
            self.sp.previous_track(device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def seek(self, position_ms: int, device_id: str | None = None) -> bool:
        """Seek to position in current track."""
        self._ensure_authenticated()
        try:
            self.sp.seek_track(position_ms, device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def set_volume(self, volume_percent: int, device_id: str | None = None) -> bool:
        """Set playback volume (0-100)."""
        self._ensure_authenticated()
        volume_percent = max(0, min(100, volume_percent))
        try:
            self.sp.volume(volume_percent, device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def toggle_shuffle(self, device_id: str | None = None) -> bool:
        """Toggle shuffle mode."""
        self._ensure_authenticated()
        state = self.get_playback_state()
        if state:
            try:
                self.sp.shuffle(not state.shuffle_state, device_id=device_id)
                return True
            except spotipy.SpotifyException:
                pass
        return False

    def cycle_repeat(self, device_id: str | None = None) -> str:
        """Cycle through repeat modes: off -> context -> track -> off."""
        self._ensure_authenticated()
        state = self.get_playback_state()
        if state:
            next_state = {
                "off": "context",
                "context": "track",
                "track": "off",
            }.get(state.repeat_state, "off")
            try:
                self.sp.repeat(next_state, device_id=device_id)
                return next_state
            except spotipy.SpotifyException:
                pass
        return "off"

    def play_uri(
        self,
        uri: str,
        device_id: str | None = None,
        context_uri: str | None = None,
        offset: int | None = None,
    ) -> bool:
        """Play a specific URI (track, album, playlist, artist)."""
        self._ensure_authenticated()
        try:
            if uri.startswith("spotify:track:"):
                # Single track
                if context_uri:
                    self.sp.start_playback(
                        device_id=device_id,
                        context_uri=context_uri,
                        offset={"uri": uri} if offset is None else {"position": offset},
                    )
                else:
                    self.sp.start_playback(device_id=device_id, uris=[uri])
            else:
                # Context (album, playlist, artist)
                kwargs: dict[str, Any] = {"device_id": device_id, "context_uri": uri}
                if offset is not None:
                    kwargs["offset"] = {"position": offset}
                self.sp.start_playback(**kwargs)
            return True
        except spotipy.SpotifyException:
            return False

    # ========================
    # Devices
    # ========================

    def get_devices(self) -> list[dict[str, Any]]:
        """Get available playback devices."""
        self._ensure_authenticated()
        try:
            result = self.sp.devices()
            return result.get("devices", [])
        except spotipy.SpotifyException:
            return []

    def transfer_playback(self, device_id: str, force_play: bool = False) -> bool:
        """Transfer playback to a device."""
        self._ensure_authenticated()
        try:
            self.sp.transfer_playback(device_id, force_play=force_play)
            return True
        except spotipy.SpotifyException:
            return False

    # ========================
    # Library
    # ========================

    def get_user_playlists(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """Get user's playlists."""
        self._ensure_authenticated()
        try:
            return self.sp.current_user_playlists(limit=limit, offset=offset)
        except spotipy.SpotifyException:
            return {"items": [], "total": 0}

    def get_playlist_tracks(
        self, playlist_id: str, limit: int = 100, offset: int = 0
    ) -> dict[str, Any]:
        """Get tracks from a playlist."""
        self._ensure_authenticated()
        try:
            return self.sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
        except spotipy.SpotifyException:
            return {"items": [], "total": 0}

    def get_playlist(self, playlist_id: str) -> dict[str, Any] | None:
        """Get playlist details."""
        self._ensure_authenticated()
        try:
            return self.sp.playlist(playlist_id)
        except spotipy.SpotifyException:
            return None

    def get_saved_tracks(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """Get user's saved tracks."""
        self._ensure_authenticated()
        try:
            return self.sp.current_user_saved_tracks(limit=limit, offset=offset)
        except spotipy.SpotifyException:
            return {"items": [], "total": 0}

    def get_saved_albums(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """Get user's saved albums."""
        self._ensure_authenticated()
        try:
            return self.sp.current_user_saved_albums(limit=limit, offset=offset)
        except spotipy.SpotifyException:
            return {"items": [], "total": 0}

    def get_followed_artists(self, limit: int = 50, after: str | None = None) -> dict[str, Any]:
        """Get user's followed artists."""
        self._ensure_authenticated()
        try:
            return self.sp.current_user_followed_artists(limit=limit, after=after)
        except spotipy.SpotifyException:
            return {"artists": {"items": [], "total": 0}}

    def save_track(self, track_id: str) -> bool:
        """Save a track to library."""
        self._ensure_authenticated()
        try:
            self.sp.current_user_saved_tracks_add([track_id])
            return True
        except spotipy.SpotifyException:
            return False

    def remove_saved_track(self, track_id: str) -> bool:
        """Remove a track from library."""
        self._ensure_authenticated()
        try:
            self.sp.current_user_saved_tracks_delete([track_id])
            return True
        except spotipy.SpotifyException:
            return False

    def is_track_saved(self, track_id: str) -> bool:
        """Check if a track is saved."""
        self._ensure_authenticated()
        try:
            result = self.sp.current_user_saved_tracks_contains([track_id])
            return result[0] if result else False
        except spotipy.SpotifyException:
            return False

    # ========================
    # Albums & Artists
    # ========================

    def get_album(self, album_id: str) -> dict[str, Any] | None:
        """Get album details."""
        self._ensure_authenticated()
        try:
            return self.sp.album(album_id)
        except spotipy.SpotifyException:
            return None

    def get_album_tracks(self, album_id: str, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """Get tracks from an album."""
        self._ensure_authenticated()
        try:
            return self.sp.album_tracks(album_id, limit=limit, offset=offset)
        except spotipy.SpotifyException:
            return {"items": [], "total": 0}

    def get_artist(self, artist_id: str) -> dict[str, Any] | None:
        """Get artist details."""
        self._ensure_authenticated()
        try:
            return self.sp.artist(artist_id)
        except spotipy.SpotifyException:
            return None

    def get_artist_top_tracks(self, artist_id: str, country: str = "US") -> list[dict[str, Any]]:
        """Get artist's top tracks."""
        self._ensure_authenticated()
        try:
            result = self.sp.artist_top_tracks(artist_id, country=country)
            return result.get("tracks", [])
        except spotipy.SpotifyException:
            return []

    def get_artist_albums(self, artist_id: str, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """Get artist's albums."""
        self._ensure_authenticated()
        try:
            return self.sp.artist_albums(artist_id, limit=limit, offset=offset)
        except spotipy.SpotifyException:
            return {"items": [], "total": 0}

    # ========================
    # Search
    # ========================

    def search(
        self,
        query: str,
        types: list[str] | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search Spotify."""
        self._ensure_authenticated()
        types = types or ["track", "album", "artist", "playlist"]
        try:
            return self.sp.search(
                q=query,
                type=",".join(types),
                limit=limit,
                offset=offset,
            )
        except spotipy.SpotifyException:
            return {}

    # ========================
    # Recently Played
    # ========================

    def get_recently_played(self, limit: int = 50) -> dict[str, Any]:
        """Get recently played tracks."""
        self._ensure_authenticated()
        try:
            return self.sp.current_user_recently_played(limit=limit)
        except spotipy.SpotifyException:
            return {"items": []}

    # ========================
    # User Profile
    # ========================

    def get_current_user(self) -> dict[str, Any] | None:
        """Get current user profile."""
        self._ensure_authenticated()
        try:
            return self.sp.current_user()
        except spotipy.SpotifyException:
            return None

    # ========================
    # Queue
    # ========================

    def add_to_queue(self, uri: str, device_id: str | None = None) -> bool:
        """Add a track to the queue."""
        self._ensure_authenticated()
        try:
            self.sp.add_to_queue(uri, device_id=device_id)
            return True
        except spotipy.SpotifyException:
            return False

    def get_queue(self) -> dict[str, Any]:
        """Get the user's queue."""
        self._ensure_authenticated()
        try:
            return self.sp.queue()
        except spotipy.SpotifyException:
            return {"currently_playing": None, "queue": []}
