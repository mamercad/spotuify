"""Tests for the configuration module."""

import json
import pytest
from pathlib import Path
from typing import Any
from unittest.mock import patch, MagicMock

from spotuify.utils.config import Config


class TestConfig:
    """Tests for Config class."""

    def test_config_creates_directories(self, tmp_path: Path) -> None:
        """Test that Config creates necessary directories."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        assert config_dir.exists()
        assert cache_dir.exists()

    def test_config_loads_existing_file(
        self, tmp_path: Path, sample_config_data: dict[str, Any]
    ) -> None:
        """Test loading configuration from existing file."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"
        config_dir.mkdir(parents=True)
        cache_dir.mkdir(parents=True)

        config_file = config_dir / "config.json"
        with open(config_file, "w") as f:
            json.dump(sample_config_data, f)

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        assert config.client_id == "test_client_id"
        assert config.client_secret == "test_client_secret"
        assert config.redirect_uri == "http://localhost:8888/callback"

    def test_config_uses_defaults_when_no_file(self, tmp_path: Path) -> None:
        """Test that default values are used when no config file exists."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        assert config.client_id == ""
        assert config.client_secret == ""
        assert config.redirect_uri == "http://localhost:8888/callback"

    def test_config_handles_invalid_json(self, tmp_path: Path) -> None:
        """Test handling of invalid JSON in config file."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"
        config_dir.mkdir(parents=True)
        cache_dir.mkdir(parents=True)

        config_file = config_dir / "config.json"
        with open(config_file, "w") as f:
            f.write("{ invalid json }")

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        # Should fall back to defaults
        assert config.client_id == ""

    def test_config_save(self, tmp_path: Path) -> None:
        """Test saving configuration to file."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()
                config.client_id = "new_client_id"
                config.client_secret = "new_secret"
                config.save()

        # Verify file was written
        config_file = config_dir / "config.json"
        with open(config_file) as f:
            saved_data = json.load(f)

        assert saved_data["client_id"] == "new_client_id"
        assert saved_data["client_secret"] == "new_secret"

    def test_config_get_set(self, tmp_path: Path) -> None:
        """Test get and set methods."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        # Test get with default
        assert config.get("nonexistent", "default") == "default"

        # Test set and get
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"

    def test_config_client_id_property(self, tmp_path: Path) -> None:
        """Test client_id property getter and setter."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        config.client_id = "test_id"
        assert config.client_id == "test_id"

    def test_config_client_secret_property(self, tmp_path: Path) -> None:
        """Test client_secret property getter and setter."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        config.client_secret = "test_secret"
        assert config.client_secret == "test_secret"

    def test_config_redirect_uri_property(self, tmp_path: Path) -> None:
        """Test redirect_uri property getter and setter."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        config.redirect_uri = "http://custom:9999/callback"
        assert config.redirect_uri == "http://custom:9999/callback"

    def test_config_token_cache_path(self, tmp_path: Path) -> None:
        """Test token_cache_path property."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        expected_path = str(cache_dir / ".spotify_token_cache")
        assert config.token_cache_path == expected_path

    def test_config_scopes(self, tmp_path: Path) -> None:
        """Test scopes property returns space-separated string."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        scopes = config.scopes
        assert isinstance(scopes, str)
        assert "user-read-playback-state" in scopes
        assert "user-modify-playback-state" in scopes
        assert " " in scopes  # Space-separated

    def test_config_is_configured_false(self, tmp_path: Path) -> None:
        """Test is_configured returns False when credentials missing."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()

        assert config.is_configured() is False

    def test_config_is_configured_true(self, tmp_path: Path) -> None:
        """Test is_configured returns True when credentials present."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()
                config.client_id = "test_id"
                config.client_secret = "test_secret"

        assert config.is_configured() is True

    def test_config_is_configured_partial(self, tmp_path: Path) -> None:
        """Test is_configured returns False when only partial credentials."""
        config_dir = tmp_path / "config"
        cache_dir = tmp_path / "cache"

        with patch("spotuify.utils.config.user_config_dir", return_value=str(config_dir)):
            with patch("spotuify.utils.config.user_cache_dir", return_value=str(cache_dir)):
                config = Config()
                config.client_id = "test_id"
                # No client_secret

        assert config.is_configured() is False
