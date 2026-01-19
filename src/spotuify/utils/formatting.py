"""Formatting utilities for Spotuify."""

from typing import Any


def format_duration(ms: int | None) -> str:
    """Format duration from milliseconds to MM:SS format."""
    if ms is None:
        return "--:--"

    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


def format_track_info(track: dict[str, Any] | None) -> str:
    """Format track information for display."""
    if not track:
        return "No track playing"

    name = track.get("name", "Unknown")
    artists = track.get("artists", [])
    artist_names = ", ".join(a.get("name", "Unknown") for a in artists)

    return f"{name} - {artist_names}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with a suffix."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def format_artist_names(artists: list[dict[str, Any]]) -> str:
    """Format a list of artists to a comma-separated string."""
    return ", ".join(a.get("name", "Unknown") for a in artists)


def format_play_count(count: int | None) -> str:
    """Format play count with appropriate suffix (K, M, B)."""
    if count is None:
        return ""

    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}B"
    elif count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def get_album_art_url(images: list[dict[str, Any]], size: str = "medium") -> str | None:
    """Get album art URL of the specified size."""
    if not images:
        return None

    # Spotify provides images in different sizes
    # Usually: 640x640, 300x300, 64x64
    if size == "large" and len(images) > 0:
        return images[0].get("url")
    elif size == "medium" and len(images) > 1:
        return images[1].get("url")
    elif size == "small" and len(images) > 2:
        return images[2].get("url")

    # Fallback to first available
    return images[0].get("url") if images else None
