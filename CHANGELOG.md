# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Spotuify TUI Spotify player
- Full playback control (play, pause, skip, seek, volume)
- Shuffle and repeat mode support
- Browse user playlists with sidebar navigation
- Search functionality for tracks, albums, artists, and playlists
- Library view with liked songs, saved albums, and followed artists
- Playlist detail view with track listing
- Album detail view with track listing
- Artist view with top tracks and discography
- Device selection for Spotify Connect devices
- Real-time playback state synchronization
- Keyboard-driven interface with comprehensive shortcuts
- Help screen with keyboard shortcut reference
- Spotify-themed dark UI
- OAuth2 authentication with token caching
- Cross-platform configuration file support
- Comprehensive test suite
- GitHub Actions CI/CD workflows for linting and testing

### Technical
- Built with Python 3.10+ using Textual and Rich
- Modular architecture with separate API, widgets, screens, and utils
- Type hints throughout the codebase
- pytest-based test suite with async support
- Ruff for linting and formatting
- mypy for type checking

## [0.1.0] - 2026-01-19

### Added
- Initial public release

---

## Version History

### Versioning Scheme

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

### Release Process

1. Update version in `pyproject.toml`
2. Update version in `src/spotuify/__init__.py`
3. Update this CHANGELOG
4. Create git tag: `git tag v0.1.0`
5. Push tag: `git push origin v0.1.0`
6. Create GitHub release
7. Publish to PyPI: `python -m build && twine upload dist/*`
