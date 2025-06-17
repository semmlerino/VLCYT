"""Tests for VLCYT managers."""

from VLCYT.managers.thread_manager import ThreadManager
from VLCYT.managers.settings_manager import SettingsManager


class TestThreadManager:
    """Tests for ThreadManager."""

    def test_thread_manager_initialization(self):
        """Test ThreadManager initialization."""
        manager = ThreadManager(max_threads=3)
        assert manager._max_threads == 3
        assert len(manager._active_threads) == 0

    def test_submit_task(self):
        """Test submitting a task."""
        manager = ThreadManager(max_threads=2)

        def test_func():
            return "test_result"

        thread = manager.submit(test_func)

        assert thread is not None
        assert thread in manager._active_threads

    def test_cancel_all_threads(self):
        """Test canceling all threads."""
        manager = ThreadManager(max_threads=2)

        def test_func():
            import time

            time.sleep(1)
            return "test"

        # Submit a task
        thread = manager.submit(test_func)

        # Cancel all threads
        manager.cancel_all_threads()

        # Verify thread was canceled
        assert thread.is_canceled()

    def test_shutdown(self):
        """Test manager shutdown."""
        manager = ThreadManager(max_threads=2)

        def test_func():
            return "test"

        # Submit a task
        manager.submit(test_func)

        # Shutdown should work without errors
        manager.shutdown()

        # Manager should be in shutdown state
        assert manager._shutdown_flag is True


class TestSettingsManager:
    """Tests for SettingsManager."""

    def test_settings_manager_initialization(self):
        """Test SettingsManager initialization."""
        from VLCYT.managers.settings_manager import QSettings

        mock_settings = QSettings("Test", "TestApp")
        manager = SettingsManager(mock_settings)
        assert manager.qsettings == mock_settings

    def test_volume_settings(self):
        """Test volume settings."""
        from VLCYT.managers.settings_manager import QSettings

        mock_settings = QSettings("Test", "TestApp")
        manager = SettingsManager(mock_settings)

        # Test setting and getting volume
        manager.set_volume(75)
        volume = manager.get_volume()
        assert volume == 75

    def test_quality_settings(self):
        """Test quality settings."""
        from VLCYT.managers.settings_manager import QSettings

        mock_settings = QSettings("Test", "TestApp")
        manager = SettingsManager(mock_settings)

        # Test setting and getting quality
        manager.set_default_quality("720p")
        quality = manager.get_default_quality()
        assert quality == "720p"
