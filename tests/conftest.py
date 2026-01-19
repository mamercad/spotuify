"""Pytest configuration and fixtures for Spotuify tests."""

import json
import pytest
from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, AsyncMock, patch

# Sample Spotify API response data for testing


@pytest.fixture
def sample_track() -> dict[str, Any]:
    """Sample track data from Spotify API."""
    return {
        "id": "track123",
        "name": "Test Track",
        "uri": "spotify:track:track123",
        "duration_ms": 210000,  # 3:30
        "artists": [
            {"id": "artist1", "name": "Test Artist"},
            {"id": "artist2", "name": "Featured Artist"},
        ],
        "album": {
            "id": "album123",
            "name": "Test Album",
            "images": [
                {"url": "https://example.com/large.jpg", "width": 640, "height": 640},
                {"url": "https://example.com/medium.jpg", "width": 300, "height": 300},
                {"url": "https://example.com/small.jpg", "width": 64, "height": 64},
            ],
            "release_date": "2023-01-15",
        },
        "popularity": 75,
    }


@pytest.fixture
def sample_track_item(sample_track: dict[str, Any]) -> dict[str, Any]:
    """Sample track item as returned in playlists (with 'track' wrapper)."""
    return {
        "added_at": "2023-06-15T10:30:00Z",
        "track": sample_track,
    }


@pytest.fixture
def sample_album() -> dict[str, Any]:
    """Sample album data from Spotify API."""
    return {
        "id": "album123",
        "name": "Test Album",
        "uri": "spotify:album:album123",
        "album_type": "album",
        "total_tracks": 12,
        "release_date": "2023-01-15",
        "artists": [
            {"id": "artist1", "name": "Test Artist"},
        ],
        "images": [
            {"url": "https://example.com/large.jpg", "width": 640, "height": 640},
            {"url": "https://example.com/medium.jpg", "width": 300, "height": 300},
        ],
        "tracks": {
            "items": [],
            "total": 12,
        },
    }


@pytest.fixture
def sample_artist() -> dict[str, Any]:
    """Sample artist data from Spotify API."""
    return {
        "id": "artist1",
        "name": "Test Artist",
        "uri": "spotify:artist:artist1",
        "genres": ["rock", "alternative", "indie"],
        "popularity": 80,
        "followers": {
            "total": 1500000,
        },
        "images": [
            {"url": "https://example.com/artist_large.jpg", "width": 640, "height": 640},
        ],
    }


@pytest.fixture
def sample_playlist() -> dict[str, Any]:
    """Sample playlist data from Spotify API."""
    return {
        "id": "playlist123",
        "name": "My Test Playlist",
        "uri": "spotify:playlist:playlist123",
        "description": "A test playlist for testing purposes",
        "owner": {
            "id": "user123",
            "display_name": "Test User",
        },
        "tracks": {
            "items": [],
            "total": 50,
        },
        "images": [
            {"url": "https://example.com/playlist.jpg", "width": 300, "height": 300},
        ],
        "public": True,
        "collaborative": False,
    }


@pytest.fixture
def sample_device() -> dict[str, Any]:
    """Sample device data from Spotify API."""
    return {
        "id": "device123",
        "name": "My Computer",
        "type": "Computer",
        "is_active": True,
        "is_private_session": False,
        "is_restricted": False,
        "volume_percent": 65,
    }


@pytest.fixture
def sample_devices(sample_device: dict[str, Any]) -> list[dict[str, Any]]:
    """List of sample devices."""
    return [
        sample_device,
        {
            "id": "device456",
            "name": "Living Room Speaker",
            "type": "Speaker",
            "is_active": False,
            "is_private_session": False,
            "is_restricted": False,
            "volume_percent": 50,
        },
        {
            "id": "device789",
            "name": "My Phone",
            "type": "Smartphone",
            "is_active": False,
            "is_private_session": False,
            "is_restricted": False,
            "volume_percent": 75,
        },
    ]


@pytest.fixture
def sample_playback_state(
    sample_track: dict[str, Any], sample_device: dict[str, Any]
) -> dict[str, Any]:
    """Sample playback state from Spotify API."""
    return {
        "is_playing": True,
        "item": sample_track,
        "device": sample_device,
        "progress_ms": 45000,  # 0:45
        "shuffle_state": False,
        "repeat_state": "off",
        "context": {
            "type": "playlist",
            "uri": "spotify:playlist:playlist123",
        },
    }


@pytest.fixture
def sample_user() -> dict[str, Any]:
    """Sample user profile data."""
    return {
        "id": "user123",
        "display_name": "Test User",
        "email": "test@example.com",
        "country": "US",
        "product": "premium",
        "followers": {
            "total": 100,
        },
        "images": [
            {"url": "https://example.com/user.jpg", "width": 300, "height": 300},
        ],
    }


@pytest.fixture
def sample_search_results(
    sample_track: dict[str, Any],
    sample_album: dict[str, Any],
    sample_artist: dict[str, Any],
    sample_playlist: dict[str, Any],
) -> dict[str, Any]:
    """Sample search results from Spotify API."""
    return {
        "tracks": {
            "items": [sample_track],
            "total": 1,
            "limit": 20,
            "offset": 0,
        },
        "albums": {
            "items": [sample_album],
            "total": 1,
            "limit": 20,
            "offset": 0,
        },
        "artists": {
            "items": [sample_artist],
            "total": 1,
            "limit": 20,
            "offset": 0,
        },
        "playlists": {
            "items": [sample_playlist],
            "total": 1,
            "limit": 20,
            "offset": 0,
        },
    }


@pytest.fixture
def sample_recently_played(sample_track: dict[str, Any]) -> dict[str, Any]:
    """Sample recently played response."""
    return {
        "items": [
            {
                "track": sample_track,
                "played_at": "2023-06-15T10:30:00Z",
                "context": {
                    "type": "playlist",
                    "uri": "spotify:playlist:playlist123",
                },
            }
        ],
        "limit": 50,
    }


@pytest.fixture
def mock_spotipy() -> Generator[MagicMock, None, None]:
    """Mock the spotipy.Spotify client."""
    with patch("spotipy.Spotify") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def mock_spotify_oauth() -> Generator[MagicMock, None, None]:
    """Mock the SpotifyOAuth class."""
    with patch("spotipy.oauth2.SpotifyOAuth") as mock:
        oauth = MagicMock()
        mock.return_value = oauth
        yield oauth


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """Create a temporary config directory."""
    config_dir = tmp_path / "spotuify"
    config_dir.mkdir(parents=True)
    return config_dir


@pytest.fixture
def sample_config_data() -> dict[str, Any]:
    """Sample configuration data."""
    return {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "redirect_uri": "http://localhost:8888/callback",
        "theme": "spotify",
        "refresh_interval": 1.0,
        "show_album_art": True,
        "default_volume": 50,
    }


@pytest.fixture
def temp_config_file(temp_config_dir: Path, sample_config_data: dict[str, Any]) -> Path:
    """Create a temporary config file with sample data."""
    config_file = temp_config_dir / "config.json"
    with open(config_file, "w") as f:
        json.dump(sample_config_data, f)
    return config_file


@pytest.fixture
def sample_token_info() -> dict[str, Any]:
    """Sample OAuth token info."""
    return {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "user-read-playback-state user-modify-playback-state",
        "expires_at": 9999999999,  # Far future
    }
