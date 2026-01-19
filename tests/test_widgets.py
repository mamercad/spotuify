"""Tests for Textual widgets."""

import pytest
from typing import Any
from unittest.mock import MagicMock, patch, AsyncMock

from textual.app import App, ComposeResult
from textual.pilot import Pilot


class TestNowPlayingWidget:
    """Tests for NowPlaying widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with NowPlaying widget."""
        from spotuify.widgets.now_playing import NowPlaying

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield NowPlaying(id="now-playing")

        return TestApp

    @pytest.mark.asyncio
    async def test_now_playing_default_state(self, widget_app: type[App]) -> None:
        """Test NowPlaying widget default state."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#now-playing")
            assert widget.track_name == "No track playing"
            assert widget.artist_name == ""
            assert widget.is_playing is False

    @pytest.mark.asyncio
    async def test_now_playing_update_track(
        self, widget_app: type[App], sample_track: dict[str, Any]
    ) -> None:
        """Test updating track information."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#now-playing")

            widget.update_track(track=sample_track, is_playing=True, progress_ms=45000)

            assert widget.track_name == "Test Track"
            assert "Test Artist" in widget.artist_name
            assert widget.is_playing is True
            assert widget.progress_ms == 45000

    @pytest.mark.asyncio
    async def test_now_playing_clear_track(
        self, widget_app: type[App], sample_track: dict[str, Any]
    ) -> None:
        """Test clearing track information."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#now-playing")

            # Set a track first
            widget.update_track(track=sample_track, is_playing=True)
            # Clear it
            widget.update_track(track=None, is_playing=False)

            assert widget.track_name == "No track playing"
            assert widget.artist_name == ""


class TestPlayerControlsWidget:
    """Tests for PlayerControls widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with PlayerControls widget."""
        from spotuify.widgets.player_controls import PlayerControls

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield PlayerControls(id="controls")

        return TestApp

    @pytest.mark.asyncio
    async def test_player_controls_default_state(self, widget_app: type[App]) -> None:
        """Test PlayerControls default state."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#controls")
            assert widget.is_playing is False
            assert widget.shuffle_state is False
            assert widget.repeat_state == "off"

    @pytest.mark.asyncio
    async def test_player_controls_update_state(self, widget_app: type[App]) -> None:
        """Test updating player control states."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#controls")

            widget.update_state(is_playing=True, shuffle_state=True, repeat_state="track")

            assert widget.is_playing is True
            assert widget.shuffle_state is True
            assert widget.repeat_state == "track"

    @pytest.mark.asyncio
    async def test_player_controls_play_button_message(self, widget_app: type[App]) -> None:
        """Test that pressing play button emits PlayPause message."""
        from spotuify.widgets.player_controls import PlayerControls

        messages = []

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield PlayerControls(id="controls")

            def on_player_controls_play_pause(self, event: PlayerControls.PlayPause) -> None:
                messages.append(event)

        async with TestApp().run_test() as pilot:
            await pilot.click("#play-btn")
            assert len(messages) == 1

    @pytest.mark.asyncio
    async def test_player_controls_next_button_message(self, widget_app: type[App]) -> None:
        """Test that pressing next button emits Next message."""
        from spotuify.widgets.player_controls import PlayerControls

        messages = []

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield PlayerControls(id="controls")

            def on_player_controls_next(self, event: PlayerControls.Next) -> None:
                messages.append(event)

        async with TestApp().run_test() as pilot:
            await pilot.click("#next-btn")
            assert len(messages) == 1

    @pytest.mark.asyncio
    async def test_player_controls_previous_button_message(self, widget_app: type[App]) -> None:
        """Test that pressing previous button emits Previous message."""
        from spotuify.widgets.player_controls import PlayerControls

        messages = []

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield PlayerControls(id="controls")

            def on_player_controls_previous(self, event: PlayerControls.Previous) -> None:
                messages.append(event)

        async with TestApp().run_test() as pilot:
            await pilot.click("#prev-btn")
            assert len(messages) == 1


class TestVolumeBarWidget:
    """Tests for VolumeBar widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with VolumeBar widget."""
        from spotuify.widgets.volume_bar import VolumeBar

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield VolumeBar(id="volume")

        return TestApp

    @pytest.mark.asyncio
    async def test_volume_bar_default_state(self, widget_app: type[App]) -> None:
        """Test VolumeBar default state."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#volume")
            assert widget.volume == 50
            assert widget.is_muted is False

    @pytest.mark.asyncio
    async def test_volume_bar_set_volume(self, widget_app: type[App]) -> None:
        """Test setting volume."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#volume")

            widget.set_volume(75)

            assert widget.volume == 75

    @pytest.mark.asyncio
    async def test_volume_bar_clamps_volume(self, widget_app: type[App]) -> None:
        """Test that volume is clamped to 0-100."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#volume")

            widget.set_volume(150)
            assert widget.volume == 100

            widget.set_volume(-50)
            assert widget.volume == 0

    @pytest.mark.asyncio
    async def test_volume_bar_increase(self, widget_app: type[App]) -> None:
        """Test increasing volume."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#volume")

            widget.set_volume(50)
            widget.increase_volume(10)

            assert widget.volume == 60

    @pytest.mark.asyncio
    async def test_volume_bar_decrease(self, widget_app: type[App]) -> None:
        """Test decreasing volume."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#volume")

            widget.set_volume(50)
            widget.decrease_volume(10)

            assert widget.volume == 40

    @pytest.mark.asyncio
    async def test_volume_bar_toggle_mute(self, widget_app: type[App]) -> None:
        """Test toggling mute."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#volume")

            widget.set_volume(75)
            assert widget.is_muted is False

            widget.toggle_mute()
            assert widget.is_muted is True

            widget.toggle_mute()
            assert widget.is_muted is False


class TestPlaybackProgressWidget:
    """Tests for PlaybackProgress widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with PlaybackProgress widget."""
        from spotuify.widgets.progress_bar import PlaybackProgress

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield PlaybackProgress(id="progress")

        return TestApp

    @pytest.mark.asyncio
    async def test_progress_bar_default_state(self, widget_app: type[App]) -> None:
        """Test PlaybackProgress default state."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#progress")
            assert widget.progress_ms == 0
            assert widget.duration_ms == 0

    @pytest.mark.asyncio
    async def test_progress_bar_update(self, widget_app: type[App]) -> None:
        """Test updating progress."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#progress")

            widget.update_progress(60000, 180000)  # 1:00 / 3:00

            assert widget.progress_ms == 60000
            assert widget.duration_ms == 180000


class TestSearchBarWidget:
    """Tests for SearchBar widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with SearchBar widget."""
        from spotuify.widgets.search_bar import SearchBar

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield SearchBar(id="search")

        return TestApp

    @pytest.mark.asyncio
    async def test_search_bar_submit_message(self, widget_app: type[App]) -> None:
        """Test that submitting search emits SearchSubmitted message."""
        from spotuify.widgets.search_bar import SearchBar

        messages = []

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield SearchBar(id="search")

            def on_search_bar_search_submitted(self, event: SearchBar.SearchSubmitted) -> None:
                messages.append(event.query)

        async with TestApp().run_test() as pilot:
            # Type in search box and submit
            search_input = pilot.app.query_one("#search-input")
            search_input.value = "test query"
            await pilot.press("enter")

            # Wait for message processing
            await pilot.pause()
            assert "test query" in messages

    @pytest.mark.asyncio
    async def test_search_bar_get_query(self, widget_app: type[App]) -> None:
        """Test getting current query."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#search")
            search_input = app.query_one("#search-input")

            search_input.value = "my search"

            assert widget.get_query() == "my search"

    @pytest.mark.asyncio
    async def test_search_bar_clear(self, widget_app: type[App]) -> None:
        """Test clearing search."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#search")
            search_input = app.query_one("#search-input")

            search_input.value = "my search"
            widget.clear_search()

            assert widget.get_query() == ""


class TestSidebarWidget:
    """Tests for Sidebar widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with Sidebar widget."""
        from spotuify.widgets.sidebar import Sidebar

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield Sidebar(id="sidebar")

        return TestApp

    @pytest.mark.asyncio
    async def test_sidebar_default_nav_items(self, widget_app: type[App]) -> None:
        """Test Sidebar has default navigation items."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#sidebar")

            # Check that nav list exists
            nav_list = app.query_one("#nav-list")
            assert nav_list is not None

    @pytest.mark.asyncio
    async def test_sidebar_set_playlists(
        self, widget_app: type[App], sample_playlist: dict[str, Any]
    ) -> None:
        """Test setting playlists in sidebar."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#sidebar")

            widget.set_playlists([sample_playlist])

            assert len(widget.playlists) == 1
            assert widget.playlists[0]["name"] == "My Test Playlist"

    @pytest.mark.asyncio
    async def test_sidebar_item_selected_message(self, widget_app: type[App]) -> None:
        """Test that selecting item emits ItemSelected message."""
        from spotuify.widgets.sidebar import Sidebar

        messages = []

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield Sidebar(id="sidebar")

            def on_sidebar_item_selected(self, event: Sidebar.ItemSelected) -> None:
                messages.append((event.item_id, event.item_type))

        async with TestApp().run_test() as pilot:
            # Navigate to and select an item
            nav_list = pilot.app.query_one("#nav-list")
            # Focus the list and press enter on first item
            nav_list.focus()
            await pilot.press("enter")
            await pilot.pause()

            assert len(messages) >= 1


class TestDeviceSelectorWidget:
    """Tests for DeviceSelector widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with DeviceSelector widget."""
        from spotuify.widgets.device_selector import DeviceSelector

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield DeviceSelector(id="devices")

        return TestApp

    @pytest.mark.asyncio
    async def test_device_selector_default_state(self, widget_app: type[App]) -> None:
        """Test DeviceSelector default state."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#devices")
            assert widget.devices == []
            assert widget.active_device_id is None

    @pytest.mark.asyncio
    async def test_device_selector_set_devices(
        self, widget_app: type[App], sample_devices: list[dict[str, Any]]
    ) -> None:
        """Test setting devices in selector."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#devices")

            widget.set_devices(sample_devices)

            assert len(widget.devices) == 3
            # Active device should be detected
            assert widget.active_device_id == "device123"

    @pytest.mark.asyncio
    async def test_device_selector_empty_devices(self, widget_app: type[App]) -> None:
        """Test selector with no devices."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#devices")

            widget.set_devices([])

            # No devices label should be visible
            no_devices = app.query_one("#no-devices")
            assert no_devices.display is True


class TestTrackListWidget:
    """Tests for TrackList widget."""

    @pytest.fixture
    def widget_app(self) -> type[App]:
        """Create a test app with TrackList widget."""
        from spotuify.widgets.track_list import TrackList

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield TrackList(id="tracks")

        return TestApp

    @pytest.mark.asyncio
    async def test_track_list_default_state(self, widget_app: type[App]) -> None:
        """Test TrackList default state."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#tracks")
            assert widget.tracks == []
            assert widget.context_uri is None
            assert widget.current_track_id is None

    @pytest.mark.asyncio
    async def test_track_list_set_tracks(
        self, widget_app: type[App], sample_track_item: dict[str, Any]
    ) -> None:
        """Test setting tracks in list."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#tracks")

            widget.set_tracks(
                [sample_track_item],
                context_uri="spotify:playlist:test123",
            )

            assert len(widget.tracks) == 1
            assert widget.context_uri == "spotify:playlist:test123"

    @pytest.mark.asyncio
    async def test_track_list_set_current_track(
        self, widget_app: type[App], sample_track_item: dict[str, Any]
    ) -> None:
        """Test setting current playing track."""
        async with widget_app().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#tracks")

            widget.set_tracks([sample_track_item])
            widget.set_current_track("track123")

            assert widget.current_track_id == "track123"

    @pytest.mark.asyncio
    async def test_track_list_track_selected_message(
        self, widget_app: type[App], sample_track_item: dict[str, Any]
    ) -> None:
        """Test that selecting track emits TrackSelected message."""
        from spotuify.widgets.track_list import TrackList

        messages = []

        class TestApp(App):
            def compose(self) -> ComposeResult:
                yield TrackList(id="tracks")

            def on_track_list_track_selected(self, event: TrackList.TrackSelected) -> None:
                messages.append(event.track_id)

        async with TestApp().run_test() as pilot:
            app = pilot.app
            widget = app.query_one("#tracks")
            widget.set_tracks([sample_track_item])

            # Wait for render
            await pilot.pause()

            # Select the track
            table = app.query_one("#tracks-table")
            table.focus()
            await pilot.press("enter")
            await pilot.pause()

            assert "track123" in messages
