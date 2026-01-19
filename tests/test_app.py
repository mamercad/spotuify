"""Tests for the main Spotuify application."""

import pytest
from typing import Any
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path

from textual.app import App


class TestSpotuifyApp:
    """Tests for SpotuifyApp class."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> MagicMock:
        """Create a mock config."""
        config = MagicMock()
        config.client_id = "test_client_id"
        config.client_secret = "test_client_secret"
        config.redirect_uri = "http://localhost:8888/callback"
        config.is_configured.return_value = True
        config.config_file = tmp_path / "config.json"
        return config

    @pytest.fixture
    def mock_spotify_client(self) -> MagicMock:
        """Create a mock Spotify client."""
        client = MagicMock()
        client.authenticate.return_value = True
        client.is_authenticated.return_value = True
        client.get_playback_state.return_value = None
        client.get_user_playlists.return_value = {"items": [], "total": 0}
        return client

    @pytest.mark.asyncio
    async def test_app_creates_config(self) -> None:
        """Test that app creates config on initialization."""
        with patch("spotuify.app.Config") as mock_config_class:
            with patch("spotuify.app.SpotifyClient"):
                from spotuify.app import SpotuifyApp

                app = SpotuifyApp()
                mock_config_class.assert_called_once()

    @pytest.mark.asyncio
    async def test_app_has_correct_title(self) -> None:
        """Test app has correct title."""
        with patch("spotuify.app.Config"):
            with patch("spotuify.app.SpotifyClient"):
                from spotuify.app import SpotuifyApp

                app = SpotuifyApp()
                assert app.TITLE == "Spotuify"

    @pytest.mark.asyncio
    async def test_app_has_screens_defined(self) -> None:
        """Test app has required screens defined."""
        with patch("spotuify.app.Config"):
            with patch("spotuify.app.SpotifyClient"):
                from spotuify.app import SpotuifyApp

                app = SpotuifyApp()
                assert "main" in app.SCREENS
                assert "search" in app.SCREENS
                assert "library" in app.SCREENS
                assert "devices" in app.SCREENS
                assert "help" in app.SCREENS

    @pytest.mark.asyncio
    async def test_app_has_quit_binding(self) -> None:
        """Test app has quit keybinding."""
        with patch("spotuify.app.Config"):
            with patch("spotuify.app.SpotifyClient"):
                from spotuify.app import SpotuifyApp

                app = SpotuifyApp()
                binding_keys = [b.key for b in app.BINDINGS]
                assert "q" in binding_keys

    @pytest.mark.asyncio
    async def test_app_mounts_with_mock_spotify(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test app mounts successfully with mocked Spotify."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    # App should have started
                    assert app.is_running

    @pytest.mark.asyncio
    async def test_app_shows_warning_when_not_configured(self, tmp_path: Path) -> None:
        """Test app shows warning when credentials not configured."""
        mock_config = MagicMock()
        mock_config.is_configured.return_value = False
        mock_config.config_file = tmp_path / "config.json"

        notifications = []

        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient"):
                from spotuify.app import SpotuifyApp

                class TestApp(SpotuifyApp):
                    def notify(self, message: str, **kwargs: Any) -> None:
                        notifications.append(message)
                        super().notify(message, **kwargs)

                async with TestApp().run_test() as pilot:
                    await pilot.pause()

        assert any("configure" in n.lower() for n in notifications)

    @pytest.mark.asyncio
    async def test_action_toggle_play(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test toggle play action calls Spotify client."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_toggle_play()

                    mock_spotify_client.toggle_playback.assert_called_once()

    @pytest.mark.asyncio
    async def test_action_next_track(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test next track action calls Spotify client."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_next_track()

                    mock_spotify_client.next_track.assert_called_once()

    @pytest.mark.asyncio
    async def test_action_previous_track(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test previous track action calls Spotify client."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_previous_track()

                    mock_spotify_client.previous_track.assert_called_once()

    @pytest.mark.asyncio
    async def test_action_volume_up(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test volume up action calls Spotify client."""
        from spotuify.api.client import PlaybackState

        mock_spotify_client.get_playback_state.return_value = PlaybackState(volume_percent=50)

        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_volume_up()

                    mock_spotify_client.set_volume.assert_called_once_with(55, None)

    @pytest.mark.asyncio
    async def test_action_volume_down(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test volume down action calls Spotify client."""
        from spotuify.api.client import PlaybackState

        mock_spotify_client.get_playback_state.return_value = PlaybackState(volume_percent=50)

        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_volume_down()

                    mock_spotify_client.set_volume.assert_called_once_with(45, None)

    @pytest.mark.asyncio
    async def test_action_toggle_shuffle(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test toggle shuffle action calls Spotify client."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_toggle_shuffle()

                    mock_spotify_client.toggle_shuffle.assert_called_once()

    @pytest.mark.asyncio
    async def test_action_cycle_repeat(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test cycle repeat action calls Spotify client."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.action_cycle_repeat()

                    mock_spotify_client.cycle_repeat.assert_called_once()

    @pytest.mark.asyncio
    async def test_play_uri(self, mock_config: MagicMock, mock_spotify_client: MagicMock) -> None:
        """Test play_uri method calls Spotify client."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.play_uri("spotify:track:abc123")

                    mock_spotify_client.play_uri.assert_called_once_with(
                        "spotify:track:abc123",
                        device_id=None,
                        context_uri=None,
                        offset=None,
                    )

    @pytest.mark.asyncio
    async def test_play_uri_with_context(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test play_uri with context URI."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.play_uri(
                        "spotify:track:abc123",
                        context_uri="spotify:playlist:xyz",
                        offset=5,
                    )

                    mock_spotify_client.play_uri.assert_called_once_with(
                        "spotify:track:abc123",
                        device_id=None,
                        context_uri="spotify:playlist:xyz",
                        offset=5,
                    )

    @pytest.mark.asyncio
    async def test_push_screen_playlist(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test push_screen creates PlaylistScreen with ID."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp
                from spotuify.screens.playlist import PlaylistScreen

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.push_screen("playlist", {"playlist_id": "test123"})
                    await pilot.pause()

                    assert isinstance(app.screen, PlaylistScreen)
                    assert app.screen.playlist_id == "test123"

    @pytest.mark.asyncio
    async def test_push_screen_album(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test push_screen creates AlbumScreen with ID."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp
                from spotuify.screens.album import AlbumScreen

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.push_screen("album", {"album_id": "album123"})
                    await pilot.pause()

                    assert isinstance(app.screen, AlbumScreen)
                    assert app.screen.album_id == "album123"

    @pytest.mark.asyncio
    async def test_push_screen_artist(
        self, mock_config: MagicMock, mock_spotify_client: MagicMock
    ) -> None:
        """Test push_screen creates ArtistScreen with ID."""
        with patch("spotuify.app.Config", return_value=mock_config):
            with patch("spotuify.app.SpotifyClient", return_value=mock_spotify_client):
                from spotuify.app import SpotuifyApp
                from spotuify.screens.artist import ArtistScreen

                async with SpotuifyApp().run_test() as pilot:
                    app = pilot.app
                    app.spotify = mock_spotify_client

                    app.push_screen("artist", {"artist_id": "artist1"})
                    await pilot.pause()

                    assert isinstance(app.screen, ArtistScreen)
                    assert app.screen.artist_id == "artist1"


class TestMainEntryPoint:
    """Tests for main entry point."""

    def test_main_function_exists(self) -> None:
        """Test that main function exists."""
        from spotuify.__main__ import main

        assert callable(main)

    def test_main_returns_int(self) -> None:
        """Test that main function returns an integer (when mocked)."""
        with patch("spotuify.__main__.SpotuifyApp") as mock_app_class:
            mock_app = MagicMock()
            mock_app_class.return_value = mock_app

            from spotuify.__main__ import main

            result = main()

            assert result == 0
            mock_app.run.assert_called_once()
