"""Tests for the formatting utilities module."""

import pytest
from typing import Any

from spotuify.utils.formatting import (
    format_duration,
    format_track_info,
    truncate_text,
    format_artist_names,
    format_play_count,
    get_album_art_url,
)


class TestFormatDuration:
    """Tests for format_duration function."""

    def test_format_duration_none(self) -> None:
        """Test formatting None returns placeholder."""
        assert format_duration(None) == "--:--"

    def test_format_duration_zero(self) -> None:
        """Test formatting zero milliseconds."""
        assert format_duration(0) == "0:00"

    def test_format_duration_under_minute(self) -> None:
        """Test formatting duration under one minute."""
        assert format_duration(30000) == "0:30"
        assert format_duration(5000) == "0:05"
        assert format_duration(59000) == "0:59"

    def test_format_duration_exact_minute(self) -> None:
        """Test formatting exactly one minute."""
        assert format_duration(60000) == "1:00"

    def test_format_duration_minutes_and_seconds(self) -> None:
        """Test formatting minutes and seconds."""
        assert format_duration(90000) == "1:30"
        assert format_duration(210000) == "3:30"
        assert format_duration(185000) == "3:05"

    def test_format_duration_long_track(self) -> None:
        """Test formatting longer durations."""
        assert format_duration(600000) == "10:00"
        assert format_duration(3600000) == "60:00"

    def test_format_duration_with_milliseconds_truncated(self) -> None:
        """Test that milliseconds are properly truncated."""
        assert format_duration(90500) == "1:30"
        assert format_duration(90999) == "1:30"


class TestFormatTrackInfo:
    """Tests for format_track_info function."""

    def test_format_track_info_none(self) -> None:
        """Test formatting None track."""
        assert format_track_info(None) == "No track playing"

    def test_format_track_info_empty_dict(self) -> None:
        """Test formatting empty track dict."""
        assert format_track_info({}) == "Unknown - "

    def test_format_track_info_single_artist(self, sample_track: dict[str, Any]) -> None:
        """Test formatting track with single artist."""
        track = {
            "name": "Test Song",
            "artists": [{"name": "Test Artist"}],
        }
        assert format_track_info(track) == "Test Song - Test Artist"

    def test_format_track_info_multiple_artists(self, sample_track: dict[str, Any]) -> None:
        """Test formatting track with multiple artists."""
        result = format_track_info(sample_track)
        assert "Test Track" in result
        assert "Test Artist" in result
        assert "Featured Artist" in result

    def test_format_track_info_missing_name(self) -> None:
        """Test formatting track with missing name."""
        track = {"artists": [{"name": "Artist"}]}
        assert format_track_info(track) == "Unknown - Artist"

    def test_format_track_info_missing_artists(self) -> None:
        """Test formatting track with missing artists."""
        track = {"name": "Song Name"}
        assert format_track_info(track) == "Song Name - "


class TestTruncateText:
    """Tests for truncate_text function."""

    def test_truncate_text_short(self) -> None:
        """Test truncating text shorter than max length."""
        assert truncate_text("Hello", 10) == "Hello"

    def test_truncate_text_exact_length(self) -> None:
        """Test text exactly at max length."""
        assert truncate_text("Hello", 5) == "Hello"

    def test_truncate_text_longer(self) -> None:
        """Test truncating text longer than max length."""
        assert truncate_text("Hello World", 8) == "Hello..."

    def test_truncate_text_custom_suffix(self) -> None:
        """Test truncating with custom suffix."""
        assert truncate_text("Hello World", 9, suffix="~") == "Hello Wo~"

    def test_truncate_text_empty_suffix(self) -> None:
        """Test truncating with empty suffix."""
        assert truncate_text("Hello World", 5, suffix="") == "Hello"

    def test_truncate_text_empty_string(self) -> None:
        """Test truncating empty string."""
        assert truncate_text("", 10) == ""

    def test_truncate_text_unicode(self) -> None:
        """Test truncating unicode text."""
        assert truncate_text("Hello 🎵 World", 10) == "Hello 🎵..."


class TestFormatArtistNames:
    """Tests for format_artist_names function."""

    def test_format_artist_names_empty(self) -> None:
        """Test formatting empty artist list."""
        assert format_artist_names([]) == ""

    def test_format_artist_names_single(self) -> None:
        """Test formatting single artist."""
        artists = [{"name": "Artist One"}]
        assert format_artist_names(artists) == "Artist One"

    def test_format_artist_names_multiple(self) -> None:
        """Test formatting multiple artists."""
        artists = [
            {"name": "Artist One"},
            {"name": "Artist Two"},
            {"name": "Artist Three"},
        ]
        assert format_artist_names(artists) == "Artist One, Artist Two, Artist Three"

    def test_format_artist_names_missing_name(self) -> None:
        """Test formatting artist with missing name."""
        artists = [{"id": "123"}]
        assert format_artist_names(artists) == "Unknown"

    def test_format_artist_names_mixed(self) -> None:
        """Test formatting mix of valid and invalid artists."""
        artists = [
            {"name": "Valid Artist"},
            {"id": "no_name"},
        ]
        assert format_artist_names(artists) == "Valid Artist, Unknown"


class TestFormatPlayCount:
    """Tests for format_play_count function."""

    def test_format_play_count_none(self) -> None:
        """Test formatting None play count."""
        assert format_play_count(None) == ""

    def test_format_play_count_small(self) -> None:
        """Test formatting small numbers."""
        assert format_play_count(0) == "0"
        assert format_play_count(100) == "100"
        assert format_play_count(999) == "999"

    def test_format_play_count_thousands(self) -> None:
        """Test formatting thousands."""
        assert format_play_count(1000) == "1.0K"
        assert format_play_count(1500) == "1.5K"
        assert format_play_count(999999) == "1000.0K"

    def test_format_play_count_millions(self) -> None:
        """Test formatting millions."""
        assert format_play_count(1000000) == "1.0M"
        assert format_play_count(1500000) == "1.5M"
        assert format_play_count(999999999) == "1000.0M"

    def test_format_play_count_billions(self) -> None:
        """Test formatting billions."""
        assert format_play_count(1000000000) == "1.0B"
        assert format_play_count(2500000000) == "2.5B"


class TestGetAlbumArtUrl:
    """Tests for get_album_art_url function."""

    def test_get_album_art_url_empty(self) -> None:
        """Test getting URL from empty images list."""
        assert get_album_art_url([]) is None

    def test_get_album_art_url_large(self) -> None:
        """Test getting large image URL."""
        images = [
            {"url": "https://large.jpg", "width": 640},
            {"url": "https://medium.jpg", "width": 300},
            {"url": "https://small.jpg", "width": 64},
        ]
        assert get_album_art_url(images, "large") == "https://large.jpg"

    def test_get_album_art_url_medium(self) -> None:
        """Test getting medium image URL."""
        images = [
            {"url": "https://large.jpg", "width": 640},
            {"url": "https://medium.jpg", "width": 300},
            {"url": "https://small.jpg", "width": 64},
        ]
        assert get_album_art_url(images, "medium") == "https://medium.jpg"

    def test_get_album_art_url_small(self) -> None:
        """Test getting small image URL."""
        images = [
            {"url": "https://large.jpg", "width": 640},
            {"url": "https://medium.jpg", "width": 300},
            {"url": "https://small.jpg", "width": 64},
        ]
        assert get_album_art_url(images, "small") == "https://small.jpg"

    def test_get_album_art_url_fallback(self) -> None:
        """Test fallback when requested size not available."""
        images = [{"url": "https://only.jpg", "width": 300}]
        # Should fall back to first available
        assert get_album_art_url(images, "small") == "https://only.jpg"

    def test_get_album_art_url_default_medium(self) -> None:
        """Test default size is medium."""
        images = [
            {"url": "https://large.jpg", "width": 640},
            {"url": "https://medium.jpg", "width": 300},
        ]
        assert get_album_art_url(images) == "https://medium.jpg"
