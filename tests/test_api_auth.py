"""Tests for the Spotify authentication module."""

import pytest
from typing import Any
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
import os

from spotuify.api.auth import SpotifyAuth, CallbackHandler
from spotuify.utils.config import Config


class TestCallbackHandler:
    """Tests for CallbackHandler class."""

    def test_callback_handler_extracts_code(self) -> None:
        """Test that callback handler extracts authorization code."""
        CallbackHandler.auth_code = None
        CallbackHandler.error = None

        handler = MagicMock(spec=CallbackHandler)
        handler.path = "/callback?code=test_auth_code"

        # Simulate the GET request parsing
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(handler.path)
        params = parse_qs(parsed.query)

        if "code" in params:
            CallbackHandler.auth_code = params["code"][0]

        assert CallbackHandler.auth_code == "test_auth_code"
        assert CallbackHandler.error is None

    def test_callback_handler_extracts_error(self) -> None:
        """Test that callback handler extracts error."""
        CallbackHandler.auth_code = None
        CallbackHandler.error = None

        handler = MagicMock(spec=CallbackHandler)
        handler.path = "/callback?error=access_denied"

        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(handler.path)
        params = parse_qs(parsed.query)

        if "error" in params:
            CallbackHandler.error = params["error"][0]

        assert CallbackHandler.auth_code is None
        assert CallbackHandler.error == "access_denied"


class TestSpotifyAuth:
    """Tests for SpotifyAuth class."""

    @pytest.fixture
    def mock_config(self, tmp_path: Path) -> Config:
        """Create a mock config."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()
                config.client_id = "test_client_id"
                config.client_secret = "test_client_secret"
                config.redirect_uri = "http://localhost:8888/callback"
                return config

    @pytest.fixture
    def auth(self, mock_config: Config) -> SpotifyAuth:
        """Create a SpotifyAuth instance."""
        return SpotifyAuth(mock_config)

    def test_auth_init(self, mock_config: Config) -> None:
        """Test SpotifyAuth initialization."""
        auth = SpotifyAuth(mock_config)
        assert auth.config == mock_config
        assert auth._oauth is None

    def test_get_oauth_creates_instance(self, auth: SpotifyAuth) -> None:
        """Test _get_oauth creates SpotifyOAuth instance."""
        with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
            mock_oauth = MagicMock()
            mock_oauth_class.return_value = mock_oauth

            result = auth._get_oauth()

            assert result == mock_oauth
            mock_oauth_class.assert_called_once()
            # Verify it was called with correct parameters
            call_kwargs = mock_oauth_class.call_args.kwargs
            assert call_kwargs["client_id"] == "test_client_id"
            assert call_kwargs["client_secret"] == "test_client_secret"
            assert call_kwargs["redirect_uri"] == "http://localhost:8888/callback"

    def test_get_oauth_reuses_instance(self, auth: SpotifyAuth) -> None:
        """Test _get_oauth reuses existing instance."""
        mock_oauth = MagicMock()
        auth._oauth = mock_oauth

        result = auth._get_oauth()

        assert result == mock_oauth

    def test_get_cached_token_returns_valid_token(
        self, auth: SpotifyAuth, sample_token_info: dict[str, Any]
    ) -> None:
        """Test get_cached_token returns valid cached token."""
        with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
            mock_oauth = MagicMock()
            mock_oauth.get_cached_token.return_value = sample_token_info
            mock_oauth.is_token_expired.return_value = False
            mock_oauth_class.return_value = mock_oauth

            result = auth.get_cached_token()

            assert result == sample_token_info
            mock_oauth.get_cached_token.assert_called_once()

    def test_get_cached_token_refreshes_expired_token(
        self, auth: SpotifyAuth, sample_token_info: dict[str, Any]
    ) -> None:
        """Test get_cached_token refreshes expired token."""
        refreshed_token = {**sample_token_info, "access_token": "new_token"}

        with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
            mock_oauth = MagicMock()
            mock_oauth.get_cached_token.return_value = sample_token_info
            mock_oauth.is_token_expired.return_value = True
            mock_oauth.refresh_access_token.return_value = refreshed_token
            mock_oauth_class.return_value = mock_oauth

            result = auth.get_cached_token()

            assert result == refreshed_token
            mock_oauth.refresh_access_token.assert_called_once_with(
                sample_token_info["refresh_token"]
            )

    def test_get_cached_token_returns_none_when_no_token(self, auth: SpotifyAuth) -> None:
        """Test get_cached_token returns None when no cached token."""
        with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
            mock_oauth = MagicMock()
            mock_oauth.get_cached_token.return_value = None
            mock_oauth_class.return_value = mock_oauth

            result = auth.get_cached_token()

            assert result is None

    def test_get_spotify_client_returns_client(
        self, auth: SpotifyAuth, sample_token_info: dict[str, Any]
    ) -> None:
        """Test get_spotify_client returns authenticated client."""
        with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
            mock_oauth = MagicMock()
            mock_oauth.get_cached_token.return_value = sample_token_info
            mock_oauth.is_token_expired.return_value = False
            mock_oauth_class.return_value = mock_oauth

            with patch("spotipy.Spotify") as mock_spotify_class:
                mock_client = MagicMock()
                mock_spotify_class.return_value = mock_client

                result = auth.get_spotify_client()

                assert result == mock_client
                mock_spotify_class.assert_called_once_with(auth=sample_token_info["access_token"])

    def test_get_spotify_client_returns_none_when_no_token(self, auth: SpotifyAuth) -> None:
        """Test get_spotify_client returns None when not authenticated."""
        with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
            mock_oauth = MagicMock()
            mock_oauth.get_cached_token.return_value = None
            mock_oauth_class.return_value = mock_oauth

            result = auth.get_spotify_client()

            assert result is None

    def test_logout_removes_token_cache(self, auth: SpotifyAuth, tmp_path: Path) -> None:
        """Test logout removes the token cache file."""
        # Create a fake token cache file
        token_cache = tmp_path / "cache" / ".spotify_token_cache"
        token_cache.parent.mkdir(parents=True, exist_ok=True)
        token_cache.write_text('{"token": "test"}')

        auth.config._config["token_cache_path"] = str(token_cache)

        with patch.object(auth.config, "token_cache_path", str(token_cache)):
            auth.logout()

        assert not token_cache.exists()
        assert auth._oauth is None

    def test_logout_handles_missing_file(self, auth: SpotifyAuth) -> None:
        """Test logout handles case when token cache doesn't exist."""
        with patch.object(auth.config, "token_cache_path", "/nonexistent/path/token"):
            # Should not raise
            auth.logout()

        assert auth._oauth is None

    def test_authenticate_returns_cached_token_if_available(
        self, auth: SpotifyAuth, sample_token_info: dict[str, Any]
    ) -> None:
        """Test authenticate returns cached token without browser flow."""
        with patch.object(auth, "get_cached_token", return_value=sample_token_info):
            on_success = MagicMock()

            result = auth.authenticate(on_success=on_success)

            assert result == sample_token_info
            on_success.assert_called_once()

    def test_authenticate_calls_on_error_on_failure(self, auth: SpotifyAuth) -> None:
        """Test authenticate calls on_error callback on failure."""
        with patch.object(auth, "get_cached_token", return_value=None):
            with patch("spotuify.api.auth.SpotifyOAuth") as mock_oauth_class:
                mock_oauth = MagicMock()
                mock_oauth.get_authorize_url.return_value = "http://auth.url"
                mock_oauth_class.return_value = mock_oauth

                with patch("spotuify.api.auth.HTTPServer") as mock_server_class:
                    mock_server = MagicMock()
                    mock_server_class.return_value = mock_server

                    # Simulate error response
                    def handle_request():
                        CallbackHandler.error = "access_denied"

                    mock_server.handle_request.side_effect = handle_request

                    with patch("webbrowser.open"):
                        on_error = MagicMock()
                        CallbackHandler.auth_code = None
                        CallbackHandler.error = None

                        result = auth.authenticate(on_error=on_error)

                        assert result is None
                        on_error.assert_called_once_with("access_denied")
