"""
Tab container component for VLCYT.

This module contains the TabContainer class which manages all application tabs
and provides a unified interface for tab operations.
"""

try:
    from PySide6.QtWidgets import (
        QTabWidget,
        QVBoxLayout,
        QWidget,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    class QWidget:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

    class QVBoxLayout:
        def __init__(self, parent=None):
            pass

        def setContentsMargins(self, *args):
            pass

        def addWidget(self, widget):
            pass

    class QTabWidget:
        def __init__(self, parent=None):
            pass

        def addTab(self, widget, title):
            pass

        def currentIndex(self):
            return 0

        def setCurrentIndex(self, index):
            pass


from ...constants import STANDARD_MARGIN
from .history_tab import HistoryTab
from .info_tab import InfoTab
from .playlist_tab import PlaylistTab
from .transcript_tab import TranscriptTab


class TabContainer(QWidget):
    """
    Container for all application tabs.

    Provides:
    - Unified tab management
    - Tab switching and state management
    - Easy access to all tab components
    """

    def __init__(self, parent=None):
        """
        Initialize tab container.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
        self._create_tabs()

    def _setup_ui(self):
        """Setup tab container UI."""
        self.setObjectName("tabsContainer")

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            STANDARD_MARGIN, STANDARD_MARGIN // 2, STANDARD_MARGIN, STANDARD_MARGIN
        )

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

    def _create_tabs(self):
        """Create and add all tabs."""
        # Create tab instances
        self.info_tab = InfoTab()
        self.playlist_tab = PlaylistTab()
        self.transcript_tab = TranscriptTab()
        self.history_tab = HistoryTab()

        # Add tabs to the tab widget
        self.tabs.addTab(self.info_tab, "Video Info")
        self.tabs.addTab(self.playlist_tab, "Playlist")
        self.tabs.addTab(self.transcript_tab, "Transcript")
        self.tabs.addTab(self.history_tab, "History")

    def get_info_tab(self):
        """Get the info tab instance."""
        return self.info_tab

    def get_playlist_tab(self):
        """Get the playlist tab instance."""
        return self.playlist_tab

    def get_transcript_tab(self):
        """Get the transcript tab instance."""
        return self.transcript_tab

    def get_history_tab(self):
        """Get the history tab instance."""
        return self.history_tab

    def get_current_tab_index(self):
        """Get the current tab index."""
        return self.tabs.currentIndex()

    def set_current_tab_index(self, index: int):
        """
        Set the current tab index.

        Args:
            index: Tab index to switch to
        """
        self.tabs.setCurrentIndex(index)

    def handle_video_loaded(self, video_info=None):
        """
        Update all tabs when a video is loaded.

        Args:
            video_info: Video information dictionary
        """
        self.info_tab.handle_video_loaded(video_info)
        self.playlist_tab.handle_video_loaded(video_info)
        self.transcript_tab.handle_video_loaded(video_info)
        self.history_tab.handle_video_loaded(video_info)

    def handle_playback_state_changed(self, is_playing, is_paused):
        """
        Handle playback state changes across all tabs.

        Args:
            is_playing: Whether media is loaded/playing
            is_paused: Whether playback is paused
        """
        self.info_tab.handle_playback_state_changed(is_playing, is_paused)
        self.playlist_tab.handle_playback_state_changed(is_playing, is_paused)
        self.transcript_tab.handle_playback_state_changed(is_playing, is_paused)
        self.history_tab.handle_playback_state_changed(is_playing, is_paused)

    def save_all_tab_states(self):
        """Save state for all tabs."""
        self.info_tab.save_state()
        self.playlist_tab.save_state()
        self.transcript_tab.save_state()
        self.history_tab.save_state()

    def restore_all_tab_states(self):
        """Restore state for all tabs."""
        self.info_tab.restore_state()
        self.playlist_tab.restore_state()
        self.transcript_tab.restore_state()
        self.history_tab.restore_state()
