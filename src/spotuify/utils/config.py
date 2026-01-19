"""Configuration management for Spotuify."""

import json
from pathlib import Path
from typing import Any

from platformdirs import user_config_dir, user_cache_dir


class Config:
    """Manages application configuration and credentials."""

    APP_NAME = "spotuify"

    # Spotify API scopes needed for playback control
    SCOPES = [
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "user-library-read",
        "user-library-modify",
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-public",
        "playlist-modify-private",
        "user-read-recently-played",
        "user-top-read",
        "streaming",
    ]

    def __init__(self) -> None:
        self.config_dir = Path(user_config_dir(self.APP_NAME))
        self.cache_dir = Path(user_cache_dir(self.APP_NAME))
        self.config_file = self.config_dir / "config.json"
        self.token_cache_file = self.cache_dir / ".spotify_token_cache"

        self._ensure_dirs()
        self._config: dict[str, Any] = self._load_config()

    def _ensure_dirs(self) -> None:
        """Ensure configuration and cache directories exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return self._default_config()
        return self._default_config()

    def _default_config(self) -> dict[str, Any]:
        """Return default configuration."""
        return {
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "http://localhost:8888/callback",
            "theme": "spotify",
            "refresh_interval": 1.0,
            "show_album_art": True,
            "default_volume": 50,
        }

    def save(self) -> None:
        """Save configuration to file."""
        with open(self.config_file, "w") as f:
            json.dump(self._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value

    @property
    def client_id(self) -> str:
        """Get Spotify client ID."""
        return self._config.get("client_id", "")

    @client_id.setter
    def client_id(self, value: str) -> None:
        """Set Spotify client ID."""
        self._config["client_id"] = value

    @property
    def client_secret(self) -> str:
        """Get Spotify client secret."""
        return self._config.get("client_secret", "")

    @client_secret.setter
    def client_secret(self, value: str) -> None:
        """Set Spotify client secret."""
        self._config["client_secret"] = value

    @property
    def redirect_uri(self) -> str:
        """Get OAuth redirect URI."""
        return self._config.get("redirect_uri", "http://localhost:8888/callback")

    @redirect_uri.setter
    def redirect_uri(self, value: str) -> None:
        """Set OAuth redirect URI."""
        self._config["redirect_uri"] = value

    @property
    def token_cache_path(self) -> str:
        """Get the path to the token cache file."""
        return str(self.token_cache_file)

    @property
    def scopes(self) -> str:
        """Get Spotify API scopes as a space-separated string."""
        return " ".join(self.SCOPES)

    def is_configured(self) -> bool:
        """Check if Spotify credentials are configured."""
        return bool(self.client_id and self.client_secret)
