# Spotuify

[![Lint](https://github.com/mamercad/spotuify/actions/workflows/lint.yml/badge.svg)](https://github.com/mamercad/spotuify/actions/workflows/lint.yml)
[![Test](https://github.com/mamercad/spotuify/actions/workflows/test.yml/badge.svg)](https://github.com/mamercad/spotuify/actions/workflows/test.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A comprehensive Terminal User Interface (TUI) Spotify player built with Python, Textual, and Rich. Control your Spotify playback directly from the terminal with a beautiful, keyboard-driven interface.

## Screenshots

### Main Interface
```
┌─────────────────────────────────────── Spotuify ────────────────────────────────────────┐
│                                                                                          │
│ ┌─ Menu ──────────┐  ┌─ Home ─────────────────────────────────────────────────────────┐ │
│ │                 │  │                                                                 │ │
│ │  🏠 Home        │  │  #  │ Title                │ Artist          │ Album   │ Time  │ │
│ │  🔍 Search      │  │ ────┼──────────────────────┼─────────────────┼─────────┼────── │ │
│ │  📚 Library     │  │  ▶1 │ Bohemian Rhapsody    │ Queen           │ A Night │ 5:55  │ │
│ │  🕐 Recent      │  │  2  │ Hotel California     │ Eagles          │ Hotel C │ 6:30  │ │
│ │  📱 Devices     │  │  3  │ Stairway to Heaven   │ Led Zeppelin    │ Led Zep │ 8:02  │ │
│ │                 │  │  4  │ Imagine              │ John Lennon     │ Imagine │ 3:07  │ │
│ │ ─ Your Library ─│  │  5  │ Billie Jean          │ Michael Jackson │ Thrille │ 4:54  │ │
│ │  ❤️  Liked Songs │  │  6  │ Sweet Child O' Mine  │ Guns N' Roses   │ Appetit │ 5:56  │ │
│ │  💿 Albums      │  │  7  │ Smells Like Teen...  │ Nirvana         │ Neverm  │ 5:01  │ │
│ │  👤 Artists     │  │  8  │ Yesterday            │ The Beatles     │ Help!   │ 2:05  │ │
│ │                 │  │  9  │ Purple Rain          │ Prince          │ Purple  │ 8:41  │ │
│ │ ─ Playlists ────│  │ 10  │ Wonderwall           │ Oasis           │ (What's │ 4:18  │ │
│ │  🎵 Discover We │  │                                                                 │ │
│ │  🎵 Road Trip   │  │                                                                 │ │
│ │  🎵 Chill Vibes │  │                                                                 │ │
│ │  🎵 Workout Mix │  │                                                                 │ │
│ │  🎵 Focus Flow  │  │                                                                 │ │
│ └─────────────────┘  └─────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ▶ Now Playing                                                        🔊 ██████████░░░  │
│  Bohemian Rhapsody                    🔀   ⏮   ▶   ⏭   🔁                         75%  │
│  Queen • A Night at the Opera                                                            │
│                                    1:45  advancement━━━━━━━━━░░░░░░░░░░░░░░░░░░░░ 5:55                                    │
│                                                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Space Play │ n Next │ p Prev │ s Search │ l Library │ d Devices │ ? Help │ q Quit       │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Search Screen
```
┌─────────────────────────────────────── Search ──────────────────────────────────────────┐
│                                                                                          │
│  🔍 Search: queen                                                                        │
│                                                                                          │
│  ┌─ Tracks ─┬─ Albums ─┬─ Artists ─┬─ Playlists ─┐                                       │
│  │          │          │           │             │                                       │
│  ├──────────┴──────────┴───────────┴─────────────┴──────────────────────────────────────┤
│  │                                                                                      │
│  │  #  │ Title                    │ Artist          │ Album              │ Duration     │
│  │ ────┼──────────────────────────┼─────────────────┼────────────────────┼──────────    │
│  │  1  │ Bohemian Rhapsody        │ Queen           │ A Night at the Op  │ 5:55         │
│  │  2  │ Don't Stop Me Now        │ Queen           │ Jazz               │ 3:29         │
│  │  3  │ Somebody to Love         │ Queen           │ A Day at the Races │ 4:56         │
│  │  4  │ We Will Rock You         │ Queen           │ News of the World  │ 2:02         │
│  │  5  │ We Are the Champions     │ Queen           │ News of the World  │ 2:59         │
│  │  6  │ Under Pressure           │ Queen           │ Hot Space          │ 4:04         │
│  │  7  │ Killer Queen             │ Queen           │ Sheer Heart Attack │ 2:57         │
│  │  8  │ Another One Bites the D  │ Queen           │ The Game           │ 3:35         │
│  │                                                                                      │
│  └──────────────────────────────────────────────────────────────────────────────────────┘
│                                                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Enter Select │ Tab Switch Tab │ / Focus Search │ Escape Back                             │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Library Screen
```
┌─────────────────────────────────────── Library ─────────────────────────────────────────┐
│                                                                                          │
│  ┌─ Liked Songs ─┬─ Albums ─┬─ Artists ─┐                                                │
│  │               │          │           │                                                │
│  ├───────────────┴──────────┴───────────┴───────────────────────────────────────────────┤
│  │                                                                                      │
│  │  #  │ Title                    │ Artist            │ Album            │ Added        │
│  │ ────┼──────────────────────────┼───────────────────┼──────────────────┼───────────   │
│  │  1  │ Blinding Lights          │ The Weeknd        │ After Hours      │ 2024-01-15   │
│  │  2  │ As It Was                │ Harry Styles      │ Harry's House    │ 2024-01-14   │
│  │  3  │ Anti-Hero               │ Taylor Swift      │ Midnights        │ 2024-01-13   │
│  │  4  │ Heat Waves               │ Glass Animals     │ Dreamland        │ 2024-01-12   │
│  │  5  │ Levitating               │ Dua Lipa          │ Future Nostalgia │ 2024-01-11   │
│  │  6  │ Stay                     │ The Kid LAROI     │ F*CK LOVE 3      │ 2024-01-10   │
│  │  7  │ good 4 u                 │ Olivia Rodrigo    │ SOUR             │ 2024-01-09   │
│  │  8  │ Peaches                  │ Justin Bieber     │ Justice          │ 2024-01-08   │
│  │                                                                                      │
│  │                                            Showing 156 liked songs                   │
│  └──────────────────────────────────────────────────────────────────────────────────────┘
│                                                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Enter Play │ Tab Switch Tab │ r Refresh │ Escape Back                                    │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Device Selection
```
┌────────────────────────────────────── Devices ──────────────────────────────────────────┐
│                                                                                          │
│                     ┌─────────────────────────────────────────────┐                      │
│                     │                                             │                      │
│                     │        Select Playback Device               │                      │
│                     │                                             │                      │
│                     │   ● 💻 MacBook Pro                          │                      │
│                     │     Currently active                        │                      │
│                     │                                             │                      │
│                     │   ○ 📱 iPhone 15 Pro                        │                      │
│                     │                                             │                      │
│                     │   ○ 🔊 Living Room Speaker                  │                      │
│                     │                                             │                      │
│                     │   ○ 📺 Samsung TV                           │                      │
│                     │                                             │                      │
│                     │   ○ 🚗 Car Audio                            │                      │
│                     │                                             │                      │
│                     │                                             │                      │
│                     │        Press 'r' to refresh devices         │                      │
│                     │                                             │                      │
│                     └─────────────────────────────────────────────┘                      │
│                                                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Enter Select │ r Refresh │ Escape Back                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Help Screen
```
┌──────────────────────────────────────── Help ───────────────────────────────────────────┐
│                                                                                          │
│                     ┌─────────────────────────────────────────────┐                      │
│                     │                                             │                      │
│                     │     Spotuify - Keyboard Shortcuts           │                      │
│                     │                                             │                      │
│                     │  ─── Playback ───────────────────────────   │                      │
│                     │  Space      Play / Pause                    │                      │
│                     │  n          Next track                      │                      │
│                     │  p          Previous track                  │                      │
│                     │  z          Toggle shuffle                  │                      │
│                     │  r          Cycle repeat (off → all → one)  │                      │
│                     │                                             │                      │
│                     │  ─── Volume ─────────────────────────────   │                      │
│                     │  +          Volume up                       │                      │
│                     │  -          Volume down                     │                      │
│                     │  m          Toggle mute                     │                      │
│                     │                                             │                      │
│                     │  ─── Navigation ─────────────────────────   │                      │
│                     │  h          Go to Home                      │                      │
│                     │  s or /     Open Search                     │                      │
│                     │  l          Open Library                    │                      │
│                     │  d          Select device                   │                      │
│                     │  ?          Show this help                  │                      │
│                     │  Escape     Go back / Close                 │                      │
│                     │  q          Quit application                │                      │
│                     │                                             │                      │
│                     │        Press Escape or 'q' to close         │                      │
│                     │                                             │                      │
│                     └─────────────────────────────────────────────┘                      │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Features

### Playback Control
- **Play/Pause** - Control playback with a single key
- **Skip Tracks** - Navigate forward and backward through your queue
- **Seek** - Click on the progress bar to jump to any position
- **Volume Control** - Adjust volume with keyboard shortcuts
- **Shuffle & Repeat** - Toggle shuffle and cycle through repeat modes

### Browse & Discover
- **Your Library** - Access liked songs, saved albums, and followed artists
- **Playlists** - Browse and play your personal and followed playlists
- **Search** - Find tracks, albums, artists, and playlists instantly
- **Recently Played** - Quick access to your listening history

### Multi-Device Support
- **Device Selection** - Switch playback between all Spotify Connect devices
- **Real-time Sync** - UI updates automatically with playback state
- **Remote Control** - Control playback on any device from your terminal

### User Interface
- **Spotify-Themed** - Dark theme inspired by Spotify's design language
- **Keyboard-Driven** - Full control without touching the mouse
- **Responsive Layout** - Adapts to your terminal size
- **Rich Text** - Beautiful formatting with colors and Unicode symbols

## Requirements

- **Python 3.10+**
- **Spotify Premium** account (required for playback control)
- **Active Spotify Client** (desktop app, web player, or any Spotify Connect device)
- **Terminal** with Unicode support (most modern terminals)

## Installation

### Using pip (recommended)

```bash
pip install spotuify
```

### From source

```bash
git clone https://github.com/mamercad/spotuify.git
cd spotuify
pip install -e .
```

### Development installation

```bash
git clone https://github.com/mamercad/spotuify.git
cd spotuify
pip install -e ".[dev]"
```

## Quick Start

### 1. Create a Spotify Developer Application

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **"Create App"**
4. Fill in the application details:
   - **App name:** `Spotuify` (or any name you prefer)
   - **App description:** `TUI Spotify Player`
   - **Redirect URI:** `http://localhost:8888/callback`
5. Click **"Create"**
6. Go to **"Settings"** and note your **Client ID** and **Client Secret**

### 2. Configure Spotuify

Create or edit the config file:

| Platform | Config Location |
|----------|-----------------|
| Linux    | `~/.config/spotuify/config.json` |
| macOS    | `~/Library/Application Support/spotuify/config.json` |
| Windows  | `C:\Users\<user>\AppData\Local\spotuify\config.json` |

```json
{
  "client_id": "your_client_id_here",
  "client_secret": "your_client_secret_here",
  "redirect_uri": "http://localhost:8888/callback"
}
```

**Or** use environment variables:

```bash
export SPOTIPY_CLIENT_ID='your_client_id'
export SPOTIPY_CLIENT_SECRET='your_client_secret'
export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
```

### 3. Run Spotuify

```bash
spotuify
```

On first run, your browser will open to authorize the application. After authorizing, you'll be redirected back and the token will be cached for future sessions.

## Keyboard Shortcuts

### Playback

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `n` | Next track |
| `p` | Previous track |
| `z` | Toggle shuffle |
| `r` | Cycle repeat mode (off → context → track) |

### Volume

| Key | Action |
|-----|--------|
| `+` | Increase volume |
| `-` | Decrease volume |
| `m` | Toggle mute |

### Navigation

| Key | Action |
|-----|--------|
| `h` | Go to Home |
| `s` or `/` | Open Search |
| `l` | Open Library |
| `d` | Select device |
| `?` | Show help |
| `Escape` | Go back / Close modal |
| `q` | Quit application |

### List Navigation

| Key | Action |
|-----|--------|
| `↑` / `k` | Move up |
| `↓` / `j` | Move down |
| `Enter` | Select / Play |
| `Tab` | Switch tabs (in search/library) |

## Project Structure

```
spotuify/
├── src/spotuify/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point
│   ├── app.py               # Main Textual application
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # OAuth2 authentication
│   │   └── client.py        # Spotify API client wrapper
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── main.py          # Main screen with sidebar
│   │   ├── search.py        # Search screen with tabs
│   │   ├── playlist.py      # Playlist detail view
│   │   ├── album.py         # Album detail view
│   │   ├── artist.py        # Artist detail view
│   │   ├── library.py       # User library screen
│   │   ├── devices.py       # Device selection modal
│   │   └── help.py          # Help/shortcuts screen
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── now_playing.py   # Current track display
│   │   ├── player_controls.py # Playback buttons
│   │   ├── progress_bar.py  # Seekable progress bar
│   │   ├── volume_bar.py    # Volume control
│   │   ├── sidebar.py       # Navigation sidebar
│   │   ├── track_list.py    # Track listing table
│   │   ├── search_bar.py    # Search input
│   │   └── device_selector.py # Device list
│   └── utils/
│       ├── __init__.py
│       ├── config.py        # Configuration management
│       └── formatting.py    # Text formatting helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_formatting.py   # Formatting tests
│   ├── test_config.py       # Config tests
│   ├── test_api_client.py   # API client tests
│   ├── test_api_auth.py     # Auth tests
│   ├── test_widgets.py      # Widget tests
│   ├── test_screens.py      # Screen tests
│   └── test_app.py          # Integration tests
├── .github/
│   └── workflows/
│       ├── lint.yml         # Linting workflow
│       └── test.yml         # Testing workflow
├── pyproject.toml           # Project configuration
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/mamercad/spotuify.git
cd spotuify

# Install with development dependencies
pip install -e ".[dev]"
```

### Running in Development Mode

```bash
# Run with Textual dev tools (live reload, console)
textual run --dev src/spotuify/app.py:SpotuifyApp

# Or run normally
python -m spotuify

# Or use the entry point
spotuify
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=spotuify --cov-report=term-missing

# Run specific test file
pytest tests/test_api_client.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Lint code
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

### Textual Console

For debugging the TUI:

```bash
# In one terminal, run the console
textual console

# In another terminal, run the app with dev flag
textual run --dev src/spotuify/app.py:SpotuifyApp
```

## Configuration Options

The config file supports these options:

```json
{
  "client_id": "your_spotify_client_id",
  "client_secret": "your_spotify_client_secret",
  "redirect_uri": "http://localhost:8888/callback",
  "theme": "spotify",
  "refresh_interval": 1.0,
  "show_album_art": true,
  "default_volume": 50
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `client_id` | string | `""` | Spotify API client ID |
| `client_secret` | string | `""` | Spotify API client secret |
| `redirect_uri` | string | `"http://localhost:8888/callback"` | OAuth redirect URI |
| `theme` | string | `"spotify"` | UI theme (currently only "spotify") |
| `refresh_interval` | float | `1.0` | Playback state refresh interval in seconds |
| `show_album_art` | bool | `true` | Show album art (reserved for future use) |
| `default_volume` | int | `50` | Default volume level (0-100) |

## Troubleshooting

### "No devices found"

**Cause:** No active Spotify client is running.

**Solution:** 
- Open the Spotify desktop app, web player, or mobile app
- Play something briefly to wake up the device
- Press `r` in the devices screen to refresh

### "Failed to authenticate"

**Cause:** Invalid credentials or configuration.

**Solution:**
1. Verify your Client ID and Client Secret are correct
2. Ensure the redirect URI matches exactly: `http://localhost:8888/callback`
3. Delete the token cache and try again:
   - Linux/macOS: `rm ~/.cache/spotuify/.spotify_token_cache`
   - Windows: Delete `C:\Users\<user>\AppData\Local\spotuify\Cache\.spotify_token_cache`

### "Premium required"

**Cause:** Spotify Free accounts cannot control playback.

**Solution:** Upgrade to Spotify Premium to use playback control features.

### "Connection refused" or timeout errors

**Cause:** Network issues or Spotify API problems.

**Solution:**
1. Check your internet connection
2. Verify Spotify services are operational: [Spotify Status](https://status.spotify.dev/)
3. Try again in a few moments

### UI looks broken

**Cause:** Terminal doesn't support Unicode or colors.

**Solution:**
1. Use a modern terminal (iTerm2, Windows Terminal, Alacritty, Kitty)
2. Ensure your terminal supports UTF-8 encoding
3. Try setting: `export LANG=en_US.UTF-8`

## API Reference

Spotuify uses these Spotify API scopes:

- `user-read-playback-state` - Read playback state
- `user-modify-playback-state` - Control playback
- `user-read-currently-playing` - Get currently playing track
- `user-library-read` - Access saved tracks/albums
- `user-library-modify` - Save/remove tracks
- `playlist-read-private` - Access private playlists
- `playlist-read-collaborative` - Access collaborative playlists
- `user-read-recently-played` - Access recently played
- `user-top-read` - Access top tracks/artists
- `streaming` - Stream audio (reserved)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your PR:
- Passes all tests (`pytest`)
- Passes linting (`ruff check`)
- Includes tests for new functionality
- Updates documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Textual](https://textual.textualize.io/) - The amazing TUI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [Spotipy](https://spotipy.readthedocs.io/) - Spotify Web API wrapper
- [Spotify](https://developer.spotify.com/) - For providing the Web API

## Related Projects

- [spotify-tui](https://github.com/Rigellute/spotify-tui) - Spotify TUI written in Rust
- [ncspot](https://github.com/hrkfdn/ncspot) - Cross-platform ncurses Spotify client
- [spotifyd](https://github.com/Spotifyd/spotifyd) - Spotify daemon

---

Made with ❤️ and 🎵
