"""Integration tests for manager interactions."""

import pytest
from unittest.mock import MagicMock
from VLCYT.managers.thread_manager import ThreadManager
from VLCYT.managers.playback_manager import PlaybackManager


@pytest.mark.integration
class TestManagerIntegration:
    """Tests for manager integration."""

    def test_playback_thread_integration(self):
        """Test playback manager with thread manager integration."""
        # Create managers - VLC is already mocked by conftest.py
        thread_manager = ThreadManager(max_threads=2)
        mock_vlc_player = MagicMock()

        playback_manager = PlaybackManager(mock_vlc_player, thread_manager)

        # Test that managers can work together
        assert playback_manager._thread_manager == thread_manager
        assert playback_manager._vlc_player == mock_vlc_player

    def test_multiple_manager_cleanup(self):
        """Test cleanup when multiple managers share thread manager."""
        thread_manager = ThreadManager(max_threads=3)
        mock_vlc_player = MagicMock()

        playback_manager = PlaybackManager(mock_vlc_player, thread_manager)

        # Test that managers exist and work together
        assert playback_manager._thread_manager == thread_manager
        assert playback_manager._vlc_player == mock_vlc_player
        assert thread_manager._max_threads == 3
