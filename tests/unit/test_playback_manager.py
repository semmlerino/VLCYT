"""Tests for Playback Manager functionality."""

from unittest.mock import MagicMock
from VLCYT.managers.playback_manager import PlaybackManager


class TestPlaybackManager:
    """Tests for PlaybackManager class."""

    def test_playback_manager_initialization(self):
        """Test PlaybackManager initialization."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()

        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        assert manager._vlc_player == mock_vlc_player
        assert manager._thread_manager == mock_thread_manager
        assert manager._current_video_info == {}
        assert manager._is_playing is False
        assert manager._is_paused is False

    def test_play_stream(self):
        """Test play stream functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_started = MagicMock()

        stream_url = "http://example.com/stream.m3u8"
        video_info = {"title": "Test Video", "duration": 120}

        manager.play_stream(stream_url, video_info)

        assert manager._current_video_info == video_info
        assert manager._is_playing is True
        assert manager._is_paused is False
        mock_vlc_player.play.assert_called_once_with(stream_url)
        manager.playback_started.emit.assert_called_once_with(video_info)

    def test_stop_when_playing(self):
        """Test stop when currently playing."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_stopped = MagicMock()

        # Set up playing state
        manager._is_playing = True
        manager._is_paused = True

        manager.stop()

        assert manager._is_playing is False
        assert manager._is_paused is False
        mock_vlc_player.stop.assert_called_once()
        manager.playback_stopped.emit.assert_called_once()

    def test_stop_when_not_playing(self):
        """Test stop when not currently playing."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_stopped = MagicMock()

        # Ensure not playing state
        manager._is_playing = False

        manager.stop()

        # Should not call VLC stop or emit signal
        mock_vlc_player.stop.assert_not_called()
        manager.playback_stopped.emit.assert_not_called()

    def test_pause_when_playing(self):
        """Test pause when currently playing."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_paused = MagicMock()

        # Set up playing state
        manager._is_playing = True
        manager._is_paused = False

        manager.pause()

        assert manager._is_paused is True
        mock_vlc_player.pause.assert_called_once()
        manager.playback_paused.emit.assert_called_once_with(True)

    def test_pause_when_not_playing(self):
        """Test pause when not currently playing."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_paused = MagicMock()

        # Ensure not playing state
        manager._is_playing = False

        manager.pause()

        # Should not call VLC pause or emit signal
        mock_vlc_player.pause.assert_not_called()
        manager.playback_paused.emit.assert_not_called()

    def test_resume_when_paused(self):
        """Test resume when currently paused."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_paused = MagicMock()

        # Set up paused state
        manager._is_playing = True
        manager._is_paused = True

        manager.resume()

        assert manager._is_paused is False
        mock_vlc_player.play.assert_called_once()
        manager.playback_paused.emit.assert_called_once_with(False)

    def test_resume_when_not_paused(self):
        """Test resume when not currently paused."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.playback_paused = MagicMock()

        # Ensure not paused state
        manager._is_paused = False

        manager.resume()

        # Should not call VLC play or emit signal
        mock_vlc_player.play.assert_not_called()
        manager.playback_paused.emit.assert_not_called()

    def test_seek_position(self):
        """Test seek position functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)
        manager.position_changed = MagicMock()

        # Set playing state first
        manager._is_playing = True

        manager.seek(0.75)
        mock_vlc_player.set_position.assert_called_once_with(0.75)

    def test_seek_time_functionality(self):
        """Test seek time functionality."""
        mock_vlc_player = MagicMock()
        mock_vlc_player.get_length.return_value = 120000  # 2 minutes
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)
        manager.position_changed = MagicMock()

        # Set playing state first
        manager._is_playing = True

        # Seek to 60 seconds
        manager.seek_time(60)

        # Should calculate position and call set_position
        expected_position = 60 * 1000 / 120000  # 0.5
        mock_vlc_player.set_position.assert_called_once_with(expected_position)

    def test_seek_relative_functionality(self):
        """Test seek relative functionality."""
        mock_vlc_player = MagicMock()
        mock_vlc_player.get_time.return_value = 30000  # 30 seconds in ms
        mock_vlc_player.get_length.return_value = 120000  # 2 minutes in ms
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)
        manager.position_changed = MagicMock()

        # Set playing state first
        manager._is_playing = True

        # Seek forward by 10 seconds
        manager.seek_relative(10)

        # Should calculate new position and call set_position
        # new_time = 30 + 10 = 40 seconds, position = 40 * 1000 / 120000 = 0.333...
        expected_position = 40 * 1000 / 120000
        mock_vlc_player.set_position.assert_called_once_with(expected_position)

    def test_get_time_functionality(self):
        """Test get time functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        mock_vlc_player.get_time.return_value = 90000  # 90 seconds in ms

        # Set playing state first
        manager._is_playing = True

        result = manager.get_time()

        # Should return time in milliseconds as-is
        assert result == 90000

    def test_get_length_functionality(self):
        """Test get length functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        mock_vlc_player.get_length.return_value = 180000  # 3 minutes in ms

        # Set playing state first
        manager._is_playing = True

        result = manager.get_length()

        # Should return length in milliseconds as-is
        assert result == 180000

    def test_set_volume(self):
        """Test set volume functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Mock the signal
        manager.volume_changed = MagicMock()

        manager.set_volume(85)

        mock_vlc_player.set_volume.assert_called_once_with(85)
        manager.volume_changed.emit.assert_called_once_with(85)

    def test_get_volume(self):
        """Test get volume functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        mock_vlc_player.get_volume.return_value = 75

        result = manager.get_volume()
        assert result == 75

    def test_get_position_functionality(self):
        """Test get position functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        mock_vlc_player.get_position.return_value = 0.6

        # Set playing state first
        manager._is_playing = True

        result = manager.get_position()
        assert result == 0.6

    def test_get_current_video_info_functionality(self):
        """Test get current video info functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Set some video info
        video_info = {"title": "Test Video", "duration": 300}
        manager._current_video_info = video_info

        result = manager.get_current_video_info()
        assert result == video_info

    def test_is_playing_functionality(self):
        """Test is playing functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Test initial state
        assert manager.is_playing() is False

        # Test after setting to True
        manager._is_playing = True
        assert manager.is_playing() is True

    def test_is_paused_functionality(self):
        """Test is paused functionality."""
        mock_vlc_player = MagicMock()
        mock_thread_manager = MagicMock()
        manager = PlaybackManager(mock_vlc_player, mock_thread_manager)

        # Test initial state
        assert manager.is_paused() is False

        # Test after setting to True
        manager._is_paused = True
        assert manager.is_paused() is True
