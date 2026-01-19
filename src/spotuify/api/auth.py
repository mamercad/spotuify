"""Spotify OAuth authentication handler."""

import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Callable

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ..utils.config import Config


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback."""

    auth_code: str | None = None
    error: str | None = None

    def do_GET(self) -> None:
        """Handle GET request from OAuth callback."""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if "code" in params:
            CallbackHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"""
                <html>
                <head><title>Spotuify - Authorization Successful</title></head>
                <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #191414; color: #1DB954;">
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window and return to Spotuify.</p>
                </body>
                </html>
                """
            )
        elif "error" in params:
            CallbackHandler.error = params["error"][0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"""
                <html>
                <head><title>Spotuify - Authorization Failed</title></head>
                <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #191414; color: #ff4444;">
                    <h1>Authorization Failed</h1>
                    <p>Error: {CallbackHandler.error}</p>
                    <p>Please try again.</p>
                </body>
                </html>
                """.encode()
            )
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        """Suppress HTTP server logging."""
        pass


class SpotifyAuth:
    """Handles Spotify OAuth authentication flow."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._oauth: SpotifyOAuth | None = None

    def _get_oauth(self) -> SpotifyOAuth:
        """Get or create SpotifyOAuth instance."""
        if self._oauth is None:
            self._oauth = SpotifyOAuth(
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                redirect_uri=self.config.redirect_uri,
                scope=self.config.scopes,
                cache_path=self.config.token_cache_path,
                open_browser=False,
            )
        return self._oauth

    def get_cached_token(self) -> dict | None:
        """Get cached token if available and valid."""
        oauth = self._get_oauth()
        token_info = oauth.get_cached_token()

        if token_info:
            # Check if token needs refresh
            if oauth.is_token_expired(token_info):
                token_info = oauth.refresh_access_token(token_info["refresh_token"])
            return token_info
        return None

    def authenticate(
        self,
        on_waiting: Callable[[], None] | None = None,
        on_success: Callable[[], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> dict | None:
        """
        Perform OAuth authentication flow.

        Args:
            on_waiting: Callback when waiting for user authorization
            on_success: Callback when authentication succeeds
            on_error: Callback when authentication fails

        Returns:
            Token info dict if successful, None otherwise
        """
        # Check for cached token first
        token_info = self.get_cached_token()
        if token_info:
            if on_success:
                on_success()
            return token_info

        oauth = self._get_oauth()

        # Parse redirect URI for callback server
        from urllib.parse import urlparse

        parsed = urlparse(self.config.redirect_uri)
        port = parsed.port or 8888

        # Reset handler state
        CallbackHandler.auth_code = None
        CallbackHandler.error = None

        # Start callback server
        server = HTTPServer(("localhost", port), CallbackHandler)
        server.timeout = 120  # 2 minute timeout

        # Open browser for authorization
        auth_url = oauth.get_authorize_url()
        webbrowser.open(auth_url)

        if on_waiting:
            on_waiting()

        # Wait for callback
        while CallbackHandler.auth_code is None and CallbackHandler.error is None:
            server.handle_request()

        server.server_close()

        if CallbackHandler.error:
            if on_error:
                on_error(CallbackHandler.error)
            return None

        if CallbackHandler.auth_code:
            # Exchange code for token
            try:
                token_info = oauth.get_access_token(CallbackHandler.auth_code)
                if on_success:
                    on_success()
                return token_info
            except Exception as e:
                if on_error:
                    on_error(str(e))
                return None

        return None

    def get_spotify_client(self) -> spotipy.Spotify | None:
        """Get an authenticated Spotify client."""
        token_info = self.get_cached_token()
        if token_info:
            return spotipy.Spotify(auth=token_info["access_token"])
        return None

    def logout(self) -> None:
        """Remove cached token (logout)."""
        import os

        if os.path.exists(self.config.token_cache_path):
            os.remove(self.config.token_cache_path)
        self._oauth = None
