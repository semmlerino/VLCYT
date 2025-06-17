"""
Base tab component for VLCYT.

This module contains the BaseTab class which provides common functionality
for all tabs in the application.
"""

try:
    from PySide6.QtCore import QObject, Signal
    from PySide6.QtWidgets import QVBoxLayout, QWidget

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Create dummy classes for testing
    class QObject:
        pass

    class Signal:
        def __init__(self, *args):
            pass

        def connect(self, func):
            pass

        def emit(self, *args):
            pass

    class QWidget:
        def __init__(self, parent=None):
            pass

    class QVBoxLayout:
        def __init__(self, parent=None):
            pass


class BaseTab(QWidget):
    """
    Base class for all tabs in the application.

    Provides common functionality for tabs including:
    - Standard layout setup
    - State management
    - Save/restore state
    """

    def __init__(self, parent=None):
        """
        Initialize base tab.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._init_ui()
        self._is_active = False

    def _init_ui(self):
        """Initialize basic UI elements common to all tabs."""
        # Create main layout with standard margins
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

    def on_tab_activated(self):
        """
        Called when tab is activated (selected).

        Override in derived classes to handle activation.
        """
        self._is_active = True

    def on_tab_deactivated(self):
        """
        Called when another tab is activated.

        Override in derived classes to handle deactivation.
        """
        self._is_active = False

    def is_active(self) -> bool:
        """
        Check if tab is currently active.

        Returns:
            True if tab is active
        """
        return self._is_active

    def save_state(self):
        """
        Save tab state.

        Override in derived classes to save state.
        """
        pass

    def restore_state(self):
        """
        Restore tab state.

        Override in derived classes to restore state.
        """
        pass

    def handle_video_loaded(self, video_info=None):
        """
        Update tab when a video is loaded.

        Override in derived classes to handle video loading.

        Args:
            video_info: Video information dictionary
        """
        pass

    def clear(self):
        """
        Clear tab contents.

        Override in derived classes to clear contents.
        """
        pass

    def handle_playback_state_changed(self, is_playing, is_paused):
        """
        Handle playback state changes.

        Override in derived classes to react to playback state changes.

        Args:
            is_playing: Whether media is loaded/playing
            is_paused: Whether playback is paused
        """
        pass
