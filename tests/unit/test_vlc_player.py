"""Tests for VLC Player core functionality."""

from unittest.mock import patch
from VLCYT.core.vlc_player import VLCPlayer


class TestVLCPlayerBasic:
    """Tests for VLCPlayer basic functionality."""

    def test_vlc_player_initialization(self):
        """Test VLC player initialization."""
        player = VLCPlayer()

        # Basic attributes should be initialized
        assert hasattr(player, "_instance")
        assert hasattr(player, "_media_player")
        assert hasattr(player, "_media")
        assert hasattr(player, "_embed_handle")
        assert hasattr(player, "_streaming_disabled")

    def test_vlc_player_initial_state(self):
        """Test VLC player initial state."""
        player = VLCPlayer()

        # Check initial values
        assert player._media is None
        assert player._embed_handle is None
        assert player._streaming_disabled is True

    @patch("VLCYT.core.vlc_player.VLC_AVAILABLE", False)
    def test_vlc_not_available(self):
        """Test behavior when VLC is not available."""
        player = VLCPlayer()

        # Should handle gracefully when VLC not available
        assert player._instance is None
        assert player._media_player is None

    def test_setup_embedding_no_media_player(self):
        """Test embedding setup when media player is None."""
        player = VLCPlayer()
        player._media_player = None

        result = player.setup_embedding(12345)
        assert result is False

    def test_get_volume_no_media_player(self):
        """Test getting volume when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.get_volume()
        assert result == 0  # Default when no media player

    def test_get_time_no_media_player(self):
        """Test getting time when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.get_time()
        assert result == 0

    def test_get_length_no_media_player(self):
        """Test getting length when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.get_length()
        assert result == 0

    def test_get_position_no_media_player(self):
        """Test getting position when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.get_position()
        assert result == 0.0

    def test_is_playing_no_media_player(self):
        """Test is_playing when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.is_playing()
        assert result is False

    def test_play_no_media_player(self):
        """Test play when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.play("http://test.url")
        assert result is False

    def test_pause_no_media_player(self):
        """Test pause when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.pause()
        assert result is False

    def test_stop_no_media_player(self):
        """Test stop when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.stop()
        assert result is False

    def test_set_volume_no_media_player(self):
        """Test setting volume when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.set_volume(50)
        assert result is False

    def test_set_time_no_media_player(self):
        """Test setting time when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.set_time(30000)
        assert result is False

    def test_set_position_no_media_player(self):
        """Test setting position when no media player."""
        player = VLCPlayer()
        player._media_player = None

        result = player.set_position(0.5)
        assert result is False

    def test_streaming_operations_no_media_player(self):
        """Test streaming operations when no media player."""
        player = VLCPlayer()
        player._media_player = None

        # Test setup streaming
        result = player.setup_streaming(8080)
        assert isinstance(result, tuple)
        assert result[0] is False  # Should fail

        # Test disable streaming
        result = player.disable_streaming()
        assert result is False  # Should fail without media player


class TestVLCPlayerAttributes:
    """Tests for VLCPlayer attribute access."""

    def test_media_attribute_initialization(self):
        """Test media attribute initialization."""
        player = VLCPlayer()
        assert player._media is None

    def test_embed_handle_initialization(self):
        """Test embed handle initialization."""
        player = VLCPlayer()
        assert player._embed_handle is None

    def test_streaming_disabled_initialization(self):
        """Test streaming disabled initialization."""
        player = VLCPlayer()
        assert player._streaming_disabled is True

    def test_cleanup_method_exists(self):
        """Test cleanup method exists."""
        player = VLCPlayer()
        assert hasattr(player, "cleanup")

        # Should not raise exception
        player.cleanup()
