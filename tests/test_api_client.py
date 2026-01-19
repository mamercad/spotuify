"""Tests for the Spotify API client module."""

import pytest
from typing import Any
from unittest.mock import MagicMock, patch, PropertyMock

from spotuify.api.client import SpotifyClient, PlaybackState
from spotuify.utils.config import Config


class TestPlaybackState:
    """Tests for PlaybackState dataclass."""

    def test_playback_state_defaults(self) -> None:
        """Test PlaybackState default values."""
        state = PlaybackState()
        assert state.is_playing is False
        assert state.track is None
        assert state.device is None
        assert state.progress_ms == 0
        assert state.duration_ms == 0
        assert state.shuffle_state is False
        assert state.repeat_state == "off"
        assert state.volume_percent == 50
        assert state.context is None

    def test_playback_state_custom_values(
        self, sample_track: dict[str, Any], sample_device: dict[str, Any]
    ) -> None:
        """Test PlaybackState with custom values."""
        state = PlaybackState(
            is_playing=True,
            track=sample_track,
            device=sample_device,
            progress_ms=45000,
            duration_ms=210000,
            shuffle_state=True,
            repeat_state="track",
            volume_percent=75,
        )
        assert state.is_playing is True
        assert state.track == sample_track
        assert state.device == sample_device
        assert state.progress_ms == 45000
        assert state.shuffle_state is True
        assert state.repeat_state == "track"
        assert state.volume_percent == 75


class TestSpotifyClient:
    """Tests for SpotifyClient class."""

    @pytest.fixture
    def mock_config(self, tmp_path: Any) -> Config:
        """Create a mock config."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()
                config.client_id = "test_client_id"
                config.client_secret = "test_client_secret"
                return config

    @pytest.fixture
    def client(self, mock_config: Config) -> SpotifyClient:
        """Create a SpotifyClient instance."""
        return SpotifyClient(mock_config)

    def test_client_init(self, mock_config: Config) -> None:
        """Test client initialization."""
        client = SpotifyClient(mock_config)
        assert client.config == mock_config
        assert client._sp is None

    def test_client_is_authenticated_false(self, client: SpotifyClient) -> None:
        """Test is_authenticated when not authenticated."""
        assert client.is_authenticated() is False

    def test_client_is_authenticated_true(self, client: SpotifyClient) -> None:
        """Test is_authenticated when authenticated."""
        client._sp = MagicMock()
        assert client.is_authenticated() is True

    def test_client_sp_property_raises_when_not_authenticated(self, client: SpotifyClient) -> None:
        """Test sp property raises when not authenticated."""
        with pytest.raises(RuntimeError, match="Not authenticated"):
            _ = client.sp

    def test_client_sp_property_returns_client(self, client: SpotifyClient) -> None:
        """Test sp property returns client when authenticated."""
        mock_sp = MagicMock()
        client._sp = mock_sp
        assert client.sp == mock_sp

    def test_ensure_authenticated_raises(self, client: SpotifyClient) -> None:
        """Test _ensure_authenticated raises when not authenticated."""
        with pytest.raises(RuntimeError, match="Not authenticated"):
            client._ensure_authenticated()

    def test_ensure_authenticated_passes(self, client: SpotifyClient) -> None:
        """Test _ensure_authenticated passes when authenticated."""
        client._sp = MagicMock()
        client._ensure_authenticated()  # Should not raise

    # ========================
    # Playback Control Tests
    # ========================

    def test_get_playback_state(
        self, client: SpotifyClient, sample_playback_state: dict[str, Any]
    ) -> None:
        """Test get_playback_state returns correct state."""
        mock_sp = MagicMock()
        mock_sp.current_playback.return_value = sample_playback_state
        client._sp = mock_sp

        state = client.get_playback_state()

        assert state is not None
        assert state.is_playing is True
        assert state.track == sample_playback_state["item"]
        assert state.progress_ms == 45000
        mock_sp.current_playback.assert_called_once()

    def test_get_playback_state_none(self, client: SpotifyClient) -> None:
        """Test get_playback_state returns empty state when nothing playing."""
        mock_sp = MagicMock()
        mock_sp.current_playback.return_value = None
        client._sp = mock_sp

        state = client.get_playback_state()

        assert state is not None
        assert state.is_playing is False
        assert state.track is None

    def test_get_playback_state_exception(self, client: SpotifyClient) -> None:
        """Test get_playback_state returns None on exception."""
        import spotipy

        mock_sp = MagicMock()
        mock_sp.current_playback.side_effect = spotipy.SpotifyException(400, "error")
        client._sp = mock_sp

        state = client.get_playback_state()
        assert state is None

    def test_play(self, client: SpotifyClient) -> None:
        """Test play method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.play()

        assert result is True
        mock_sp.start_playback.assert_called_once_with(device_id=None)

    def test_play_with_device_id(self, client: SpotifyClient) -> None:
        """Test play with specific device."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.play(device_id="device123")

        assert result is True
        mock_sp.start_playback.assert_called_once_with(device_id="device123")

    def test_pause(self, client: SpotifyClient) -> None:
        """Test pause method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.pause()

        assert result is True
        mock_sp.pause_playback.assert_called_once_with(device_id=None)

    def test_toggle_playback_when_playing(
        self, client: SpotifyClient, sample_playback_state: dict[str, Any]
    ) -> None:
        """Test toggle_playback pauses when playing."""
        mock_sp = MagicMock()
        mock_sp.current_playback.return_value = sample_playback_state
        client._sp = mock_sp

        client.toggle_playback()

        mock_sp.pause_playback.assert_called_once()

    def test_toggle_playback_when_paused(
        self, client: SpotifyClient, sample_playback_state: dict[str, Any]
    ) -> None:
        """Test toggle_playback plays when paused."""
        sample_playback_state["is_playing"] = False
        mock_sp = MagicMock()
        mock_sp.current_playback.return_value = sample_playback_state
        client._sp = mock_sp

        client.toggle_playback()

        mock_sp.start_playback.assert_called_once()

    def test_next_track(self, client: SpotifyClient) -> None:
        """Test next_track method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.next_track()

        assert result is True
        mock_sp.next_track.assert_called_once()

    def test_previous_track(self, client: SpotifyClient) -> None:
        """Test previous_track method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.previous_track()

        assert result is True
        mock_sp.previous_track.assert_called_once()

    def test_seek(self, client: SpotifyClient) -> None:
        """Test seek method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.seek(60000)

        assert result is True
        mock_sp.seek_track.assert_called_once_with(60000, device_id=None)

    def test_set_volume(self, client: SpotifyClient) -> None:
        """Test set_volume method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.set_volume(75)

        assert result is True
        mock_sp.volume.assert_called_once_with(75, device_id=None)

    def test_set_volume_clamps_to_range(self, client: SpotifyClient) -> None:
        """Test set_volume clamps values to 0-100."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        client.set_volume(150)
        mock_sp.volume.assert_called_with(100, device_id=None)

        client.set_volume(-50)
        mock_sp.volume.assert_called_with(0, device_id=None)

    def test_toggle_shuffle(
        self, client: SpotifyClient, sample_playback_state: dict[str, Any]
    ) -> None:
        """Test toggle_shuffle method."""
        mock_sp = MagicMock()
        mock_sp.current_playback.return_value = sample_playback_state
        client._sp = mock_sp

        result = client.toggle_shuffle()

        assert result is True
        mock_sp.shuffle.assert_called_once_with(True, device_id=None)

    def test_cycle_repeat(
        self, client: SpotifyClient, sample_playback_state: dict[str, Any]
    ) -> None:
        """Test cycle_repeat cycles through modes."""
        mock_sp = MagicMock()
        sample_playback_state["repeat_state"] = "off"
        mock_sp.current_playback.return_value = sample_playback_state
        client._sp = mock_sp

        result = client.cycle_repeat()

        assert result == "context"
        mock_sp.repeat.assert_called_once_with("context", device_id=None)

    def test_play_uri_track(self, client: SpotifyClient) -> None:
        """Test play_uri with a track URI."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.play_uri("spotify:track:abc123")

        assert result is True
        mock_sp.start_playback.assert_called_once_with(
            device_id=None, uris=["spotify:track:abc123"]
        )

    def test_play_uri_context(self, client: SpotifyClient) -> None:
        """Test play_uri with a context URI (playlist/album)."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.play_uri("spotify:playlist:abc123")

        assert result is True
        mock_sp.start_playback.assert_called_once_with(
            device_id=None, context_uri="spotify:playlist:abc123"
        )

    # ========================
    # Devices Tests
    # ========================

    def test_get_devices(self, client: SpotifyClient, sample_devices: list[dict[str, Any]]) -> None:
        """Test get_devices returns device list."""
        mock_sp = MagicMock()
        mock_sp.devices.return_value = {"devices": sample_devices}
        client._sp = mock_sp

        devices = client.get_devices()

        assert len(devices) == 3
        assert devices[0]["name"] == "My Computer"

    def test_transfer_playback(self, client: SpotifyClient) -> None:
        """Test transfer_playback method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.transfer_playback("device123")

        assert result is True
        mock_sp.transfer_playback.assert_called_once_with("device123", force_play=False)

    # ========================
    # Library Tests
    # ========================

    def test_get_user_playlists(
        self, client: SpotifyClient, sample_playlist: dict[str, Any]
    ) -> None:
        """Test get_user_playlists method."""
        mock_sp = MagicMock()
        mock_sp.current_user_playlists.return_value = {
            "items": [sample_playlist],
            "total": 1,
        }
        client._sp = mock_sp

        result = client.get_user_playlists()

        assert result["total"] == 1
        assert len(result["items"]) == 1
        mock_sp.current_user_playlists.assert_called_once_with(limit=50, offset=0)

    def test_get_playlist_tracks(
        self, client: SpotifyClient, sample_track_item: dict[str, Any]
    ) -> None:
        """Test get_playlist_tracks method."""
        mock_sp = MagicMock()
        mock_sp.playlist_tracks.return_value = {
            "items": [sample_track_item],
            "total": 1,
        }
        client._sp = mock_sp

        result = client.get_playlist_tracks("playlist123")

        assert result["total"] == 1
        mock_sp.playlist_tracks.assert_called_once_with("playlist123", limit=100, offset=0)

    def test_get_saved_tracks(
        self, client: SpotifyClient, sample_track_item: dict[str, Any]
    ) -> None:
        """Test get_saved_tracks method."""
        mock_sp = MagicMock()
        mock_sp.current_user_saved_tracks.return_value = {
            "items": [sample_track_item],
            "total": 1,
        }
        client._sp = mock_sp

        result = client.get_saved_tracks()

        assert result["total"] == 1
        mock_sp.current_user_saved_tracks.assert_called_once()

    def test_save_track(self, client: SpotifyClient) -> None:
        """Test save_track method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.save_track("track123")

        assert result is True
        mock_sp.current_user_saved_tracks_add.assert_called_once_with(["track123"])

    def test_remove_saved_track(self, client: SpotifyClient) -> None:
        """Test remove_saved_track method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.remove_saved_track("track123")

        assert result is True
        mock_sp.current_user_saved_tracks_delete.assert_called_once_with(["track123"])

    def test_is_track_saved(self, client: SpotifyClient) -> None:
        """Test is_track_saved method."""
        mock_sp = MagicMock()
        mock_sp.current_user_saved_tracks_contains.return_value = [True]
        client._sp = mock_sp

        result = client.is_track_saved("track123")

        assert result is True

    # ========================
    # Albums & Artists Tests
    # ========================

    def test_get_album(self, client: SpotifyClient, sample_album: dict[str, Any]) -> None:
        """Test get_album method."""
        mock_sp = MagicMock()
        mock_sp.album.return_value = sample_album
        client._sp = mock_sp

        result = client.get_album("album123")

        assert result == sample_album
        mock_sp.album.assert_called_once_with("album123")

    def test_get_artist(self, client: SpotifyClient, sample_artist: dict[str, Any]) -> None:
        """Test get_artist method."""
        mock_sp = MagicMock()
        mock_sp.artist.return_value = sample_artist
        client._sp = mock_sp

        result = client.get_artist("artist1")

        assert result == sample_artist
        mock_sp.artist.assert_called_once_with("artist1")

    def test_get_artist_top_tracks(
        self, client: SpotifyClient, sample_track: dict[str, Any]
    ) -> None:
        """Test get_artist_top_tracks method."""
        mock_sp = MagicMock()
        mock_sp.artist_top_tracks.return_value = {"tracks": [sample_track]}
        client._sp = mock_sp

        result = client.get_artist_top_tracks("artist1")

        assert len(result) == 1
        mock_sp.artist_top_tracks.assert_called_once_with("artist1", country="US")

    # ========================
    # Search Tests
    # ========================

    def test_search(self, client: SpotifyClient, sample_search_results: dict[str, Any]) -> None:
        """Test search method."""
        mock_sp = MagicMock()
        mock_sp.search.return_value = sample_search_results
        client._sp = mock_sp

        result = client.search("test query")

        assert "tracks" in result
        assert "albums" in result
        mock_sp.search.assert_called_once_with(
            q="test query",
            type="track,album,artist,playlist",
            limit=20,
            offset=0,
        )

    def test_search_specific_types(self, client: SpotifyClient) -> None:
        """Test search with specific types."""
        mock_sp = MagicMock()
        mock_sp.search.return_value = {}
        client._sp = mock_sp

        client.search("test", types=["track", "album"])

        mock_sp.search.assert_called_once_with(
            q="test",
            type="track,album",
            limit=20,
            offset=0,
        )

    # ========================
    # Queue Tests
    # ========================

    def test_add_to_queue(self, client: SpotifyClient) -> None:
        """Test add_to_queue method."""
        mock_sp = MagicMock()
        client._sp = mock_sp

        result = client.add_to_queue("spotify:track:abc123")

        assert result is True
        mock_sp.add_to_queue.assert_called_once_with("spotify:track:abc123", device_id=None)

    def test_get_queue(self, client: SpotifyClient, sample_track: dict[str, Any]) -> None:
        """Test get_queue method."""
        mock_sp = MagicMock()
        mock_sp.queue.return_value = {
            "currently_playing": sample_track,
            "queue": [sample_track],
        }
        client._sp = mock_sp

        result = client.get_queue()

        assert result["currently_playing"] == sample_track
        assert len(result["queue"]) == 1

    # ========================
    # User Profile Tests
    # ========================

    def test_get_current_user(self, client: SpotifyClient, sample_user: dict[str, Any]) -> None:
        """Test get_current_user method."""
        mock_sp = MagicMock()
        mock_sp.current_user.return_value = sample_user
        client._sp = mock_sp

        result = client.get_current_user()

        assert result == sample_user
        assert result["display_name"] == "Test User"

    # ========================
    # Recently Played Tests
    # ========================

    def test_get_recently_played(
        self, client: SpotifyClient, sample_recently_played: dict[str, Any]
    ) -> None:
        """Test get_recently_played method."""
        mock_sp = MagicMock()
        mock_sp.current_user_recently_played.return_value = sample_recently_played
        client._sp = mock_sp

        result = client.get_recently_played()

        assert len(result["items"]) == 1
        mock_sp.current_user_recently_played.assert_called_once_with(limit=50)
