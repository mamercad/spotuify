"""Tests for Textual screens."""

import pytest
from typing import Any
from unittest.mock import MagicMock, patch, AsyncMock

from textual.app import App, ComposeResult


class TestMainScreen:
    """Tests for MainScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with MainScreen."""
        from spotuify.screens.main import MainScreen

        class TestApp(App):
            SCREENS = {"main": MainScreen}

            def on_mount(self) -> None:
                self.push_screen("main")

        return TestApp

    @pytest.mark.asyncio
    async def test_main_screen_renders(self, screen_app: type[App]) -> None:
        """Test MainScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            # Check key components exist
            assert app.query_one("#sidebar") is not None
            assert app.query_one("#now-playing") is not None
            assert app.query_one("#player-controls") is not None

    @pytest.mark.asyncio
    async def test_main_screen_has_content_area(self, screen_app: type[App]) -> None:
        """Test MainScreen has content area."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#main-track-list") is not None

    @pytest.mark.asyncio
    async def test_main_screen_default_title(self, screen_app: type[App]) -> None:
        """Test MainScreen default content title."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            screen = app.screen
            assert screen.content_title == "Home"


class TestSearchScreen:
    """Tests for SearchScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with SearchScreen."""
        from spotuify.screens.search import SearchScreen

        class TestApp(App):
            SCREENS = {"search": SearchScreen}

            def on_mount(self) -> None:
                self.push_screen("search")

        return TestApp

    @pytest.mark.asyncio
    async def test_search_screen_renders(self, screen_app: type[App]) -> None:
        """Test SearchScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            # Check search bar exists
            assert app.query_one("#search-bar") is not None

    @pytest.mark.asyncio
    async def test_search_screen_has_result_tabs(self, screen_app: type[App]) -> None:
        """Test SearchScreen has result tabs."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#tracks-tab") is not None
            assert app.query_one("#albums-tab") is not None
            assert app.query_one("#artists-tab") is not None
            assert app.query_one("#playlists-tab") is not None

    @pytest.mark.asyncio
    async def test_search_screen_escape_goes_back(self, screen_app: type[App]) -> None:
        """Test pressing escape pops the screen."""
        from spotuify.screens.search import SearchScreen
        from spotuify.screens.main import MainScreen

        class TestApp(App):
            SCREENS = {"main": MainScreen, "search": SearchScreen}

            def on_mount(self) -> None:
                self.push_screen("main")
                self.push_screen("search")

        async with TestApp().run_test() as pilot:
            app = pilot.app
            # Should be on search screen
            assert isinstance(app.screen, SearchScreen)

            await pilot.press("escape")
            await pilot.pause()

            # Should be back on main screen
            assert isinstance(app.screen, MainScreen)


class TestPlaylistScreen:
    """Tests for PlaylistScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with PlaylistScreen."""
        from spotuify.screens.playlist import PlaylistScreen

        class TestApp(App):
            def on_mount(self) -> None:
                self.push_screen(PlaylistScreen(playlist_id="test123"))

        return TestApp

    @pytest.mark.asyncio
    async def test_playlist_screen_renders(self, screen_app: type[App]) -> None:
        """Test PlaylistScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#playlist-title") is not None
            assert app.query_one("#playlist-tracks") is not None

    @pytest.mark.asyncio
    async def test_playlist_screen_stores_id(self, screen_app: type[App]) -> None:
        """Test PlaylistScreen stores playlist_id."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            screen = app.screen
            assert screen.playlist_id == "test123"


class TestAlbumScreen:
    """Tests for AlbumScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with AlbumScreen."""
        from spotuify.screens.album import AlbumScreen

        class TestApp(App):
            def on_mount(self) -> None:
                self.push_screen(AlbumScreen(album_id="album123"))

        return TestApp

    @pytest.mark.asyncio
    async def test_album_screen_renders(self, screen_app: type[App]) -> None:
        """Test AlbumScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#album-title") is not None
            assert app.query_one("#album-tracks") is not None

    @pytest.mark.asyncio
    async def test_album_screen_stores_id(self, screen_app: type[App]) -> None:
        """Test AlbumScreen stores album_id."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            screen = app.screen
            assert screen.album_id == "album123"


class TestArtistScreen:
    """Tests for ArtistScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with ArtistScreen."""
        from spotuify.screens.artist import ArtistScreen

        class TestApp(App):
            def on_mount(self) -> None:
                self.push_screen(ArtistScreen(artist_id="artist1"))

        return TestApp

    @pytest.mark.asyncio
    async def test_artist_screen_renders(self, screen_app: type[App]) -> None:
        """Test ArtistScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#artist-name") is not None
            assert app.query_one("#artist-top-tracks") is not None
            assert app.query_one("#artist-albums") is not None

    @pytest.mark.asyncio
    async def test_artist_screen_stores_id(self, screen_app: type[App]) -> None:
        """Test ArtistScreen stores artist_id."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            screen = app.screen
            assert screen.artist_id == "artist1"


class TestLibraryScreen:
    """Tests for LibraryScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with LibraryScreen."""
        from spotuify.screens.library import LibraryScreen

        class TestApp(App):
            SCREENS = {"library": LibraryScreen}

            def on_mount(self) -> None:
                self.push_screen("library")

        return TestApp

    @pytest.mark.asyncio
    async def test_library_screen_renders(self, screen_app: type[App]) -> None:
        """Test LibraryScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            # Check tabs exist
            assert app.query_one("#liked-tab") is not None
            assert app.query_one("#albums-tab") is not None
            assert app.query_one("#artists-tab") is not None

    @pytest.mark.asyncio
    async def test_library_screen_has_track_list(self, screen_app: type[App]) -> None:
        """Test LibraryScreen has liked tracks list."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#liked-tracks") is not None


class TestDevicesScreen:
    """Tests for DevicesScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with DevicesScreen."""
        from spotuify.screens.devices import DevicesScreen

        class TestApp(App):
            SCREENS = {"devices": DevicesScreen}

            def on_mount(self) -> None:
                self.push_screen("devices")

        return TestApp

    @pytest.mark.asyncio
    async def test_devices_screen_renders(self, screen_app: type[App]) -> None:
        """Test DevicesScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            assert app.query_one("#device-selector") is not None


class TestHelpScreen:
    """Tests for HelpScreen."""

    @pytest.fixture
    def screen_app(self) -> type[App]:
        """Create a test app with HelpScreen."""
        from spotuify.screens.help import HelpScreen

        class TestApp(App):
            SCREENS = {"help": HelpScreen}

            def on_mount(self) -> None:
                self.push_screen("help")

        return TestApp

    @pytest.mark.asyncio
    async def test_help_screen_renders(self, screen_app: type[App]) -> None:
        """Test HelpScreen renders without errors."""
        async with screen_app().run_test() as pilot:
            app = pilot.app
            # Check shortcut tables exist
            assert app.query_one("#playback-shortcuts") is not None
            assert app.query_one("#navigation-shortcuts") is not None
            assert app.query_one("#volume-shortcuts") is not None

    @pytest.mark.asyncio
    async def test_help_screen_escape_closes(self, screen_app: type[App]) -> None:
        """Test pressing escape closes help screen."""
        from spotuify.screens.help import HelpScreen
        from spotuify.screens.main import MainScreen

        class TestApp(App):
            SCREENS = {"main": MainScreen, "help": HelpScreen}

            def on_mount(self) -> None:
                self.push_screen("main")
                self.push_screen("help")

        async with TestApp().run_test() as pilot:
            app = pilot.app
            assert isinstance(app.screen, HelpScreen)

            await pilot.press("escape")
            await pilot.pause()

            assert isinstance(app.screen, MainScreen)

    @pytest.mark.asyncio
    async def test_help_screen_q_closes(self, screen_app: type[App]) -> None:
        """Test pressing q closes help screen."""
        from spotuify.screens.help import HelpScreen
        from spotuify.screens.main import MainScreen

        class TestApp(App):
            SCREENS = {"main": MainScreen, "help": HelpScreen}

            def on_mount(self) -> None:
                self.push_screen("main")
                self.push_screen("help")

        async with TestApp().run_test() as pilot:
            app = pilot.app
            assert isinstance(app.screen, HelpScreen)

            await pilot.press("q")
            await pilot.pause()

            assert isinstance(app.screen, MainScreen)
